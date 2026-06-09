"""Provision the Azure AI Search agentic-retrieval pipeline:

  1. Patch the existing `build2026-chunks` index to add an Azure OpenAI
     vectorizer (so the knowledge base can vectorize queries on the fly)
     and set the default semantic configuration.
  2. Create / update a knowledge source (`build2026-ks`) wrapping that
     index.
  3. Create / update a knowledge base (`build2026-kb`) that targets the
     knowledge source and uses AOAI gpt-4o for query planning + answer
     synthesis.

Idempotent — safe to re-run.

Uses the 2026-05-01-preview REST API because we need `filterAddOn`
(per-intent OData filtering) — that's how we keep the speaker hard-filter
in place.
"""
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import httpx

API_VERSION = "2026-05-01-preview"
INDEX_NAME = os.environ.get("AZURE_SEARCH_INDEX", "build2026-chunks")
KS_NAME = os.environ.get("AZURE_SEARCH_KS_NAME", "build2026-ks")
KB_NAME = os.environ.get("AZURE_SEARCH_KB_NAME", "build2026-kb")
VECTORIZER_NAME = "aoai-ada002-vectorizer"
SEMANTIC_CONFIG_NAME = "default-semantic"

SEARCH_ENDPOINT = os.environ["AZURE_SEARCH_ENDPOINT"].rstrip("/")
SEARCH_KEY = os.environ["AZURE_SEARCH_KEY"]
AOAI_ENDPOINT = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")
AOAI_KEY = os.environ["AZURE_OPENAI_KEY"]
EMBED_DEPLOYMENT = os.environ.get("AZURE_OPENAI_EMBED_DEPLOYMENT",
                                  "text-embedding-ada-002")
CHAT_DEPLOYMENT = os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-4o")

client = httpx.Client(timeout=60.0)
HDR = {"api-key": SEARCH_KEY, "Content-Type": "application/json"}


def step(msg: str) -> None:
    print(f"\n▶ {msg}")


def _get(url: str) -> dict:
    r = client.get(url, headers=HDR)
    r.raise_for_status()
    return r.json()


def _put(url: str, body: dict) -> dict:
    r = client.put(url, headers=HDR, json=body)
    # 200 = updated, 201 = created, 204 = updated with no body
    if r.status_code not in (200, 201, 204):
        print(f"  ✗ {r.status_code}: {r.text[:800]}")
        r.raise_for_status()
    return r.json() if r.text else {}


def patch_index_with_vectorizer() -> None:
    step(f"Patching index `{INDEX_NAME}` to add vectorizer + default semantic config")
    url = f"{SEARCH_ENDPOINT}/indexes/{INDEX_NAME}?api-version={API_VERSION}"
    idx = _get(url)

    # ETag-based optimistic concurrency (not strictly needed for solo use,
    # but good practice).
    etag = idx.get("@odata.etag")

    vs = idx.get("vectorSearch") or {}
    vectorizers = vs.get("vectorizers") or []
    has_vectorizer = any(v.get("name") == VECTORIZER_NAME for v in vectorizers)
    if not has_vectorizer:
        vectorizers.append({
            "name": VECTORIZER_NAME,
            "kind": "azureOpenAI",
            "azureOpenAIParameters": {
                "resourceUri": AOAI_ENDPOINT,
                "deploymentId": EMBED_DEPLOYMENT,
                "modelName": EMBED_DEPLOYMENT,  # for ada-002, model == deployment name
                "apiKey": AOAI_KEY,
            },
        })
        vs["vectorizers"] = vectorizers
        print(f"  + added vectorizer `{VECTORIZER_NAME}`")
    else:
        print(f"  · vectorizer `{VECTORIZER_NAME}` already present")

    # Wire the profile to point at the vectorizer
    profiles = vs.get("profiles") or []
    changed_profile = False
    for p in profiles:
        if p.get("vectorizer") != VECTORIZER_NAME:
            p["vectorizer"] = VECTORIZER_NAME
            changed_profile = True
    if changed_profile:
        print(f"  + bound profile(s) to vectorizer")
    idx["vectorSearch"] = vs

    # Set the default semantic configuration
    sem = idx.get("semantic") or {}
    if sem.get("defaultConfiguration") != SEMANTIC_CONFIG_NAME:
        sem["defaultConfiguration"] = SEMANTIC_CONFIG_NAME
        idx["semantic"] = sem
        print(f"  + set defaultConfiguration={SEMANTIC_CONFIG_NAME}")

    # Strip server-only fields before PUT
    for k in ("@odata.context", "@odata.etag", "encryptionKey"):
        idx.pop(k, None)

    _put(url, idx)
    print("  ✓ index updated")


def upsert_knowledge_source() -> None:
    step(f"Upserting knowledge source `{KS_NAME}` → index `{INDEX_NAME}`")
    url = (f"{SEARCH_ENDPOINT}/knowledgesources/{KS_NAME}"
           f"?api-version={API_VERSION}")
    body = {
        "name": KS_NAME,
        "description": ("Microsoft Build 2026 session passages — "
                        "1 row per AI-summary paragraph."),
        "kind": "searchIndex",
        "searchIndexParameters": {
            "searchIndexName": INDEX_NAME,
            "semanticConfigurationName": SEMANTIC_CONFIG_NAME,
            # Fields returned in `references[].sourceData` so the synthesizer
            # has session metadata + the passage to ground on.
            "sourceDataFields": [
                {"name": "id"},
                {"name": "sessionCode"},
                {"name": "sessionTitle"},
                {"name": "speakers"},
                {"name": "topic"},
                {"name": "passage"},
                {"name": "sessionPage"},
                {"name": "transcriptUrl"},
                {"name": "videoUrl"},
                {"name": "timestamps"},
            ],
            # Limit search to text-bearing fields. URLs/codes get matched on
            # exact equality via filterAddOn instead of pulling them into the
            # text retrieval. `passage` is the main grounding field.
            "searchFields": [
                {"name": "passage"},
                {"name": "sessionTitle"},
                {"name": "topic"},
                {"name": "speakers"},
                {"name": "sessionCode"},
                {"name": "passageVector"},
            ],
        },
    }
    _put(url, body)
    print("  ✓ knowledge source upserted")


def upsert_knowledge_base() -> None:
    step(f"Upserting knowledge base `{KB_NAME}` → uses `{CHAT_DEPLOYMENT}` for planning")
    url = (f"{SEARCH_ENDPOINT}/knowledgebases/{KB_NAME}"
           f"?api-version={API_VERSION}")
    body = {
        "name": KB_NAME,
        "description": "Build 2026 chatbot knowledge base.",
        "retrievalInstructions": (
            "You are retrieving from a catalog of Microsoft Build 2026 "
            "session AI summaries. Sessions are uniquely identified by a "
            "session code such as BRK230. Each document is one paragraph "
            "from a session AI summary, with the session's metadata "
            "attached (speakers, title, code). When the user asks 'what "
            "did <person> say' about a topic, prefer documents where that "
            "person is listed in the speakers field, and where the passage "
            "explicitly mentions or attributes the claim to that person."
        ),
        "answerInstructions": (
            "You are a Microsoft Build 2026 analyst. Answer ONLY from the "
            "provided session excerpts (the supplied references). \n\n"
            "STRICT GROUNDING RULES (never break these):\n"
            "1. Every factual claim in your answer MUST be supportable by "
            "a direct sentence in one of the reference passages. Do NOT "
            "use any background knowledge from your training — even if it "
            "is widely known to be true about Microsoft, Azure, Build, or "
            "the speakers. If the passage doesn't say it, don't include "
            "it.\n"
            "2. Do NOT embellish, paraphrase-and-extend, or add 'common "
            "sense' details. Quote or tightly paraphrase the passage. "
            "Brand/product names, version numbers, features, percentages, "
            "and dates must appear verbatim in a reference.\n"
            "3. Preserve timestamps from the passages verbatim "
            "(e.g. 00:32:00).\n"
            "4. SCOPE DISCIPLINE: When a passage describes feature A and "
            "separately feature B (or speaker X talks about topic Y and "
            "separately topic Z), do NOT imply A is part of B, or that X "
            "discussed Z. Only join two facts if a single sentence in a "
            "reference joins them. Bad example: passage says 'BRK230 "
            "covers prompt caching. BRK230 also covers batch inference and "
            "distillation.' — you may NOT write 'prompt caching is part of "
            "a broader set of tools including batch inference and "
            "distillation' unless that linkage is in the passage.\n"
            "5. If you cannot find enough grounded material to answer in "
            "≥2 sentences, give a shorter, honest answer instead of "
            "padding with adjacent context.\n\n"
            "STRICT CITATION RULES:\n"
            "6. The ONLY valid citation codes are the sessionCode values "
            "from the supplied references. Do NOT invent codes from "
            "memory. If a fact came from a reference whose sessionCode "
            "is 'BRK230', cite [BRK230]. Never write a code that didn't "
            "appear in a reference (e.g. fabricating [BRK234] just "
            "because it sounds plausible).\n"
            "7. NEVER use [ref_id:N], [1], [Source N], (ref 3), or any "
            "numeric-only citation format. ALWAYS use the bracketed "
            "session code like [BRK230] or [KEY01].\n"
            "8. Every factual claim must end with at least one bracketed "
            "[sessionCode] citation pointing to a reference that actually "
            "supports it. Sentences with NO citation are not allowed "
            "unless they are pure connective text.\n\n"
            "STRICT ATTRIBUTION RULES:\n"
            "9. If the user names a specific speaker, only attribute "
            "quotes/claims to that speaker when the reference passage "
            "TEXT contains that exact name. The speakers list at the "
            "session level is not enough — the PASSAGE itself must "
            "name them.\n"
            "10. If a passage attributes a claim to a name that is "
            "different from the user-named speaker (even a similar name "
            "or an obvious typo like 'Marcus' vs 'Mark'), do NOT silently "
            "rewrite to the user's name and do NOT include a disclaimer "
            "in the answer. Instead, omit that specific claim from your "
            "answer entirely and rely only on claims where the passage "
            "name matches the speakers field of the session.\n\n"
            "REFUSAL RULES:\n"
            "11. If no reference answers the question, plainly say so. "
            "Open with phrases like 'There is no mention of...' or "
            "'The provided session excerpts do not...'. Never fabricate "
            "an answer to fill a gap.\n\n"
            "Keep responses under 250 words. Shorter, fully-grounded "
            "answers are strongly preferred over longer answers that "
            "embellish."
        ),
        "outputMode": "answerSynthesis",
        "knowledgeSources": [{"name": KS_NAME}],
        "models": [
            {
                "kind": "azureOpenAI",
                "azureOpenAIParameters": {
                    "resourceUri": AOAI_ENDPOINT,
                    "deploymentId": CHAT_DEPLOYMENT,
                    "modelName": CHAT_DEPLOYMENT,
                    "apiKey": AOAI_KEY,
                },
            }
        ],
        "encryptionKey": None,
        "retrievalReasoningEffort": {"kind": "medium"},
    }
    _put(url, body)
    print("  ✓ knowledge base upserted")


def smoke_test() -> None:
    step("Smoke test: retrieve action")
    url = (f"{SEARCH_ENDPOINT}/knowledgebases/{KB_NAME}/retrieve"
           f"?api-version={API_VERSION}")
    body = {
        "messages": [
            {"role": "user",
             "content": [{"type": "text",
                          "text": "What did Naomi say about prompt caching?"}]},
        ],
        "knowledgeSourceParams": [
            {
                "knowledgeSourceName": KS_NAME,
                "kind": "searchIndex",
                "includeReferences": True,
                "includeReferenceSourceData": True,
            }
        ],
        "includeActivity": True,
    }
    r = client.post(url, headers=HDR, json=body)
    if r.status_code != 200:
        print(f"  ✗ retrieve failed {r.status_code}: {r.text[:1200]}")
        sys.exit(1)
    j = r.json()
    print(f"  · response_text[:400] = ", end="")
    try:
        msg = j["response"][0]["content"][0]["text"]
        print(msg[:400])
    except Exception:
        print(json.dumps(j, indent=2)[:600])
    refs = j.get("references") or []
    print(f"  · references: {len(refs)} (top sessionCodes:",
          [r.get("sourceData", {}).get("sessionCode") for r in refs[:5]], ")")
    acts = j.get("activity") or []
    print(f"  · activity steps: {len(acts)}")
    for a in acts[:8]:
        keys = {k: a[k] for k in ("type", "queryTime", "elapsedMs", "count", "query")
                if k in a}
        print(f"    - {keys}")


if __name__ == "__main__":
    patch_index_with_vectorizer()
    upsert_knowledge_source()
    upsert_knowledge_base()
    smoke_test()
    print("\n✓ done")
