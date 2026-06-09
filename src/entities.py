"""Entity extraction: detect speakers, session codes, and products mentioned in
a user query, so we can hard-filter retrieval instead of relying on BM25 alone.

This is what makes "What did Naomi say about prompt caching?" only return
sessions where Naomi is actually a speaker AND prompt caching is discussed.
"""
import re
from collections import defaultdict
from typing import Dict, List, Optional, Set, Tuple


# English stopwords + question-word fillers to strip from BM25 queries.
STOPWORDS: Set[str] = {
    "a", "an", "the", "and", "or", "but", "if", "of", "in", "on", "at",
    "to", "for", "with", "by", "from", "as", "is", "are", "was", "were",
    "be", "been", "being", "have", "has", "had", "do", "does", "did",
    "doing", "said", "say", "says", "tell", "told", "tells", "telling",
    "talked", "talks", "talk", "talking", "mention", "mentioned",
    "mentions", "discuss", "discussed", "discussing", "discusses",
    "what", "who", "when", "where", "why", "how", "which", "whose",
    "whom", "whether", "about", "regarding", "concerning",
    "i", "me", "my", "we", "our", "us", "you", "your", "they", "them",
    "their", "he", "she", "him", "her", "his", "hers", "it", "its",
    "this", "that", "these", "those", "there", "here",
    "can", "could", "would", "should", "will", "shall", "may", "might",
    "must", "ought", "need", "needs", "needed",
    "also", "any", "all", "some", "every", "each", "both", "few",
    "many", "most", "other", "another", "such", "no", "not", "nor",
    "only", "own", "same", "so", "than", "too", "very", "just",
    "please", "show", "shown", "give", "list",
    # Domain-specific filler that appears in nearly every session
    "session", "sessions", "build", "build2026", "microsoft",
    "anything", "something", "thing", "things",
}


# Indicator phrases that strongly suggest the next/prev capitalized word(s)
# are a person name.
SPEAKER_HINT_PRE = re.compile(
    r"(?ix) \b (?: what \s+ did | (?:from|by|with|for) | "
    r"according \s+ to | quote (?:s|d)? \s+ from | "
    r"per |  did | said \s+ by | speaker | spoke )\b"
)
SPEAKER_HINT_POST = re.compile(
    r"(?ix) \b (?: said | says | mentioned | talked | discussed | "
    r"introduced | demoed | demonstrated | announced | claimed | "
    r"shared | thinks | believes ) \b"
)


def build_speaker_index(sessions: List[Dict]) -> Dict[str, Set[str]]:
    """Return a dict mapping {lowercase_name_or_token -> set(session_codes)}.

    For every session speaker we add: full-name, first-name, last-name, and
    any space-delimited token of length >= 3.
    """
    idx: Dict[str, Set[str]] = defaultdict(set)
    for s in sessions:
        spk = s.get("speakers")
        if not spk:
            continue
        if isinstance(spk, list):
            people = [str(p) for p in spk if p]
        else:
            people = [p.strip() for p in str(spk).split(",") if p.strip()]
        for person in people:
            person_clean = re.sub(r"\s+", " ", person).strip()
            full_lower = person_clean.lower()
            if not full_lower:
                continue
            idx[full_lower].add(s["code"])
            tokens = [t for t in re.split(r"\W+", person_clean) if len(t) >= 3]
            for t in tokens:
                idx[t.lower()].add(s["code"])
    return idx


def detect_speakers(query: str, speaker_idx: Dict[str, Set[str]]) -> List[Tuple[str, Set[str]]]:
    """Return [(matched_token, session_codes)] for each speaker name detected
    in the query. Capitalized-token heuristic + dictionary check.
    """
    if not query:
        return []
    matches: Dict[str, Set[str]] = {}

    # 1) Look for full-name match anywhere (most precise).
    q_low = query.lower()
    for full_name, codes in speaker_idx.items():
        if " " in full_name and full_name in q_low:
            matches[full_name] = codes

    # 2) Look for capitalized tokens that are also in the speaker index.
    # We only count a single capitalized token as a name match if either
    #    (a) it's preceded/followed by a speaker hint phrase, OR
    #    (b) it's not a common English word (i.e. genuine proper noun).
    #
    # This prevents "Build" or "Foundry" from being misread as a name.
    for tok_match in re.finditer(r"\b([A-Z][a-zA-Z]{2,})\b", query):
        tok = tok_match.group(1)
        tok_low = tok.lower()
        if tok_low not in speaker_idx:
            continue
        # Skip if the lowercase token is a stopword (e.g. "Did")
        if tok_low in STOPWORDS:
            continue
        # Skip if the token is also a common product/topic word that is more
        # likely intended as a topic, e.g. "Foundry", "Windows", "Copilot".
        if tok_low in BLOCKED_AS_NAME:
            continue
        # Promote the match.
        matches[tok_low] = speaker_idx[tok_low]

    # 3) Compose result. When the user typed a full name, drop any single-token
    # name match whose codes overlap with the full-name match's codes — i.e.
    # if "Mark Russinovich" is matched, drop a separate "Mark" match.
    full_name_codes: Set[str] = set()
    full_name_keys = [k for k in matches if " " in k]
    for k in full_name_keys:
        full_name_codes |= matches[k]

    keys_sorted = sorted(matches.keys(), key=lambda k: (-len(k), k))
    final: List[Tuple[str, Set[str]]] = []
    for k in keys_sorted:
        codes = matches[k]
        if " " not in k and full_name_keys:
            # If this single-name's codes intersect with any full-name match,
            # the user likely meant the full name — skip the single-name.
            if codes & full_name_codes:
                continue
        final.append((k, codes))
    return final


# Tokens that look like names (in our speaker index) but are far more likely to
# be product/topic mentions, never speaker filters.
BLOCKED_AS_NAME: Set[str] = {
    "foundry", "windows", "copilot", "azure", "fabric", "discovery",
    "cloud", "agent", "claude", "aurora", "image", "video", "robotics",
    "build", "studio", "tools", "edge", "search", "model", "models",
    "open", "data", "code", "hub", "spark", "boost", "cobalt", "maia",
    "horizon", "rayfin", "fire",
}


SESSION_CODE_RE = re.compile(r"\b([A-Z]{2,4}\d{2,4}(?:-[A-Z0-9]+)?)\b")


def detect_session_code(query: str) -> Optional[str]:
    m = SESSION_CODE_RE.search(query.upper())
    return m.group(1) if m else None


def strip_stopwords(query: str, extra_drop: Optional[Set[str]] = None) -> str:
    extra = (extra_drop or set()) | STOPWORDS
    tokens = re.findall(r"[A-Za-z0-9_+\-]+", query)
    kept = [t for t in tokens if t.lower() not in extra and len(t) > 1]
    return " ".join(kept)


def expand_query_for_speaker(query: str, speakers: List[Tuple[str, Set[str]]]) -> str:
    """Drop the speaker tokens from the BM25 query so search focuses on the
    *topic*, not the name (we already hard-filter sessions by name)."""
    if not speakers:
        return query
    out = query
    for name, _ in speakers:
        out = re.sub(re.escape(name), " ", out, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", out).strip()


# ------------------------- Evidence-level helpers -------------------------

def speaker_aliases(full_name: str) -> Set[str]:
    """Return the canonical set of lowercase substrings that count as a
    mention of `full_name` in free text. Includes the full name, the first
    name, and the last name. Tokens shorter than 3 chars are dropped.
    """
    if not full_name:
        return set()
    full = re.sub(r"\s+", " ", full_name).strip().lower()
    out: Set[str] = {full}
    for tok in re.split(r"\W+", full):
        if len(tok) >= 3:
            out.add(tok)
    return out


def text_mentions_speaker(text: str, speaker: str,
                          extra_aliases: Optional[Set[str]] = None) -> bool:
    """True iff `text` contains a word-boundary mention of any alias of
    `speaker`. Case-insensitive. Used for evidence-level speaker purity.
    """
    if not text or not speaker:
        return False
    aliases = speaker_aliases(speaker) | (extra_aliases or set())
    low = text.lower()
    for alias in aliases:
        if not alias:
            continue
        # word-boundary match, but allow multi-word aliases as substrings
        if " " in alias:
            if alias in low:
                return True
        else:
            if re.search(r"\b" + re.escape(alias) + r"\b", low):
                return True
    return False
