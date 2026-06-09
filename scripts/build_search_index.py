"""Build the Azure AI Search index for Build 2026 sessions.

Run once after provisioning (or after refreshing data/sessions.json):

    AZURE_SEARCH_ENDPOINT=...  AZURE_SEARCH_KEY=...  \\
    AZURE_OPENAI_ENDPOINT=...  AZURE_OPENAI_KEY=...  \\
    AZURE_OPENAI_EMBED_DEPLOYMENT=text-embedding-ada-002 \\
    python scripts/build_search_index.py

Index schema (per chunk = one paragraph of one session AI summary):
- id              : key  (sessionCode + chunk index)
- sessionCode     : filterable, sortable
- sessionTitle    : searchable
- speakers        : searchable, filterable (Collection(Edm.String))
- topic           : filterable
- level           : filterable
- sessionType     : filterable
- passage         : searchable (the chunk text)
- timestamps      : extracted timestamps (e.g. ["00:32:00"])
- sessionPage     : retrievable
- transcriptUrl   : retrievable
- videoUrl        : retrievable
- passageVector   : vector field (1536 dims, ada-002 / 3-small compatible)
"""
import json
import os
import re
import sys
import time
from pathlib import Path
from typing import Dict, List

import httpx

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT))

from src.rag import AzureRAG  # noqa: E402

DATA = ROOT / "data" / "sessions.json"
SESSION_PAGE = "https://build.microsoft.com/en-US/sessions/{code}"

INDEX_DEF: Dict = {
    "name": None,  # filled in
    "fields": [
        {"name": "id", "type": "Edm.String", "key": True, "filterable": True},
        {"name": "sessionCode", "type": "Edm.String",
         "filterable": True, "sortable": True, "facetable": True,
         "searchable": True},
        {"name": "sessionTitle", "type": "Edm.String",
         "searchable": True, "retrievable": True},
        {"name": "speakers", "type": "Collection(Edm.String)",
         "searchable": True, "filterable": True, "facetable": True,
         "retrievable": True},
        {"name": "topic", "type": "Edm.String",
         "filterable": True, "facetable": True, "retrievable": True,
         "searchable": True},
        {"name": "level", "type": "Edm.String",
         "filterable": True, "facetable": True, "retrievable": True},
        {"name": "sessionType", "type": "Edm.String",
         "filterable": True, "facetable": True, "retrievable": True},
        {"name": "passage", "type": "Edm.String",
         "searchable": True, "retrievable": True, "analyzer": "en.lucene"},
        {"name": "timestamps", "type": "Collection(Edm.String)",
         "filterable": False, "retrievable": True},
        {"name": "sessionPage", "type": "Edm.String", "retrievable": True},
        {"name": "transcriptUrl", "type": "Edm.String", "retrievable": True},
        {"name": "videoUrl", "type": "Edm.String", "retrievable": True},
        {"name": "hasAiSummary", "type": "Edm.Boolean",
         "filterable": True, "facetable": True, "retrievable": True,
         "sortable": True},
        {"name": "passageVector", "type": "Collection(Edm.Single)",
         "searchable": True,
         "dimensions": int(os.environ.get("RAG_EMBED_DIM", "1536")),
         "vectorSearchProfile": "default-profile"},
    ],
    "vectorSearch": {
        "profiles": [{
            "name": "default-profile",
            "algorithm": "default-hnsw",
        }],
        "algorithms": [{
            "name": "default-hnsw",
            "kind": "hnsw",
            "hnswParameters": {
                "metric": "cosine",
                "m": 4,
                "efConstruction": 400,
                "efSearch": 500,
            },
        }],
    },
    "semantic": {
        "configurations": [{
            "name": "default-semantic",
            "prioritizedFields": {
                "titleField": {"fieldName": "sessionTitle"},
                "prioritizedContentFields": [{"fieldName": "passage"}],
                "prioritizedKeywordsFields": [
                    {"fieldName": "topic"},
                    {"fieldName": "speakers"},
                ],
            },
        }],
    },
}


TS_RE = re.compile(r"\b\d{1,2}:\d{2}(?::\d{2})?\b")


def _stringify(v) -> str:
    if v is None:
        return ""
    if isinstance(v, list):
        return ", ".join(str(x) for x in v if x)
    return str(v)


def _list_speakers(s) -> List[str]:
    spk = s.get("speakers")
    if not spk:
        return []
    if isinstance(spk, list):
        return [str(p).strip() for p in spk if p]
    return [p.strip() for p in str(spk).split(",") if p.strip()]


def chunk_session(s: Dict) -> List[Dict]:
    """Split a session AI summary into paragraph-sized chunks (one per
    'section' in the summary, splitting also on long blank gaps). Falls back
    to title+description for sessions without AI summaries so they're still
    discoverable."""
    code = s["code"]
    title = s.get("title", "")
    speakers = _list_speakers(s)
    topic_raw = s.get("topic")
    topic = (topic_raw[0] if isinstance(topic_raw, list) and topic_raw
             else _stringify(topic_raw))
    level = _stringify(s.get("level"))
    stype = _stringify(s.get("type"))
    page = SESSION_PAGE.format(code=code)
    transcript = s.get("transcript") or ""
    video = s.get("video") or ""

    summary = s.get("aiSummary") or ""
    has_ai_summary = bool(summary.strip())
    base_meta = {
        "sessionCode": code,
        "sessionTitle": title,
        "speakers": speakers,
        "topic": topic,
        "level": level,
        "sessionType": stype,
        "sessionPage": page,
        "transcriptUrl": transcript,
        "videoUrl": video,
        "hasAiSummary": has_ai_summary,
    }

    chunks: List[Dict] = []
    if summary:
        # Split by "Section heading:" pattern; if not present, by paragraph;
        # then merge to ~800 char chunks for embedding quality.
        # Strategy: split on \n\n or on "  Section: " heuristic.
        raw_paragraphs = re.split(r"\n\s*\n|(?<=[.?!])\s{2,}|\u00b6", summary)
        paragraphs = [p.strip() for p in raw_paragraphs if p and len(p.strip()) > 50]
        if not paragraphs:
            paragraphs = [summary]

        # Merge to ~600-1200 char passages
        merged = []
        cur = ""
        for p in paragraphs:
            if not cur:
                cur = p
            elif len(cur) + len(p) + 2 < 1200:
                cur = cur + " " + p
            else:
                merged.append(cur)
                cur = p
        if cur:
            merged.append(cur)

        for i, passage in enumerate(merged):
            ts = TS_RE.findall(passage)
            chunks.append({
                "id": f"{code}-{i}",
                "passage": passage,
                "timestamps": ts,
                **base_meta,
            })
    else:
        # Sessions without AI summary still indexed (title + description)
        desc = s.get("description") or ""
        passage = (title + ". " + desc).strip()
        if passage:
            chunks.append({
                "id": f"{code}-0",
                "passage": passage,
                "timestamps": [],
                **base_meta,
            })
    return chunks


def ensure_index(rag: AzureRAG, name: str):
    """Create or update the Azure AI Search index."""
    INDEX_DEF["name"] = name
    url = (f"{rag.search_endpoint.rstrip('/')}/indexes/{name}"
           f"?api-version={rag.search_api_version}")
    r = httpx.put(
        url,
        headers={"api-key": rag.search_key, "Content-Type": "application/json"},
        json=INDEX_DEF,
        timeout=60.0,
    )
    if r.status_code not in (200, 201, 204):
        print(f"index PUT failed: {r.status_code} {r.text[:600]}")
        sys.exit(1)
    print(f"✓ Index '{name}' ready")


def upload_batch(rag: AzureRAG, name: str, docs: List[Dict]):
    url = (f"{rag.search_endpoint.rstrip('/')}/indexes/{name}/docs/index"
           f"?api-version={rag.search_api_version}")
    body = {"value": [{"@search.action": "mergeOrUpload", **d} for d in docs]}
    r = httpx.post(
        url,
        headers={"api-key": rag.search_key, "Content-Type": "application/json"},
        json=body,
        timeout=120.0,
    )
    if r.status_code not in (200, 201):
        print(f"upload failed: {r.status_code} {r.text[:400]}")
        sys.exit(1)
    failed = [v for v in r.json().get("value", []) if not v.get("status")]
    if failed:
        print(f"  ⚠ {len(failed)} doc errors in batch (showing first 3):")
        for f in failed[:3]:
            print(f"    {f}")


def main():
    rag = AzureRAG()
    if not rag.is_configured():
        missing = [k for k in [
            "AZURE_SEARCH_ENDPOINT", "AZURE_SEARCH_KEY",
            "AZURE_OPENAI_ENDPOINT", "AZURE_OPENAI_KEY",
        ] if not os.environ.get(k)]
        print(f"Missing env vars: {missing}", file=sys.stderr)
        sys.exit(1)
    name = rag.search_index
    print(f"Index name: {name}")
    print(f"Search endpoint: {rag.search_endpoint}")
    print(f"AOAI endpoint: {rag.aoai_endpoint}")
    print(f"Embedding deployment: {rag.aoai_embed_deployment}")
    print()

    ensure_index(rag, name)

    # Load + chunk
    with open(DATA) as f:
        sessions = json.load(f)["sessions"]
    print(f"Loaded {len(sessions)} sessions; chunking…")
    chunks: List[Dict] = []
    for s in sessions:
        chunks.extend(chunk_session(s))
    print(f"  → {len(chunks)} chunks total")

    # Embed in batches; pace inter-batch to stay under AOAI rate limits
    BATCH = 16
    # Throttle: ~5 batches/sec is well under quota; tune if needed
    INTER_BATCH_SLEEP = float(os.environ.get("RAG_BATCH_SLEEP", "0.25"))
    print(f"Embedding {len(chunks)} chunks in batches of {BATCH} "
          f"(inter-batch sleep {INTER_BATCH_SLEEP}s)…")
    t0 = time.time()
    for i in range(0, len(chunks), BATCH):
        batch = chunks[i:i + BATCH]
        texts = [c["passage"] for c in batch]
        vectors = rag.embed(texts)  # built-in backoff
        for c, vec in zip(batch, vectors):
            c["passageVector"] = vec
        time.sleep(INTER_BATCH_SLEEP)
        if i % 80 == 0:
            elapsed = time.time() - t0
            done = i + len(batch)
            rate = done / max(elapsed, 0.01)
            eta = (len(chunks) - done) / max(rate, 0.01)
            print(f"  embedded {done}/{len(chunks)} "
                  f"({rate:.1f}/s, ETA {eta:.0f}s)")
    print(f"  done in {time.time() - t0:.1f}s")

    # Upload in batches of 50
    UP_BATCH = 50
    print(f"Uploading {len(chunks)} docs in batches of {UP_BATCH}…")
    for i in range(0, len(chunks), UP_BATCH):
        batch = chunks[i:i + UP_BATCH]
        upload_batch(rag, name, batch)
        if i % 200 == 0:
            print(f"  uploaded {i + len(batch)}/{len(chunks)}")
    print(f"\n✓ Index built: {len(chunks)} passages from {len(sessions)} sessions")


if __name__ == "__main__":
    main()
