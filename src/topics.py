"""Topic taxonomy for Microsoft Build 2026 sessions.

Each topic maps to keyword patterns. A session matches a topic if any pattern
hits its title, AI summary, or description.
"""
import re
from typing import Dict, List

TOPICS: Dict[str, Dict[str, list]] = {
    "AI Foundry": {
        "patterns": [
            r"\bfoundry\b", r"\bagent service\b", r"\bagent framework\b",
            r"\bfoundry toolkit\b", r"\bfoundry iq\b", r"\bhosted agents?\b",
            r"\bmodel router\b", r"\brubric\b", r"\bfrontier tuning\b",
        ],
        "description": "Microsoft Foundry — model catalog, Agent Service, Agent Framework, Foundry Toolkit, hosted agents, evaluations, fine-tuning",
    },
    "AI Infrastructure": {
        "patterns": [
            r"\bazure (?:context )?cache\b", r"\bprompt cach", r"\bkv cache\b",
            r"\bmanifold\b", r"\binference\b", r"\bgpu\b", r"\baccelerator\b",
            r"\bcobalt\b", r"\bmaia\b", r"\bsandbox isolation\b",
            r"\bmicrosoft execution containers?\b", r"\bmxc\b",
        ],
        "description": "Azure AI infrastructure — Maia/Cobalt silicon, Manifold, Context Cache, prompt caching, inference optimization, containers",
    },
    "Models": {
        "patterns": [
            r"\bmai-\w+\b", r"\bgpt-?\d", r"\bclaude\b", r"\bopus\b",
            r"\bsonnet\b", r"\bllama\b", r"\bmistral\b", r"\bdeepseek\b",
            r"\bphi-?\d?", r"\baurora\b", r"\bimage 2\.5\b", r"\bmodel catalog\b",
            r"\bfine-?tun", r"\bdistillation\b", r"\bfireworks\b",
        ],
        "description": "Frontier and open models — MAI family, GPT-5.x, Claude/Anthropic, Llama, Mistral, Phi, Aurora geospatial, Image 2.5",
    },
    "Agents": {
        "patterns": [
            r"\bagentic\b", r"\bagent harness\b", r"\bagent 365\b",
            r"\bautopilot\b", r"\bscout\b", r"\bopenclaw\b", r"\bclaw\b",
            r"\bcopilot studio\b", r"\bmulti-?agent\b", r"\bmcp\b",
            r"\btoolbox\b", r"\bagent control\b", r"\bassert\b",
        ],
        "description": "Agent platforms and patterns — Agent 365, Autopilot, Scout, Claw + Agent Harness, OpenClaw, MCP, Toolbox, ACS, ASSERT",
    },
    "Windows": {
        "patterns": [
            r"\bwindows\b", r"\bwsl\b", r"\bwsl ?containers?\b", r"\bwslc\b",
            r"\bcopilot\+? ?pc\b", r"\bsurface\b", r"\bsnapdragon\b",
            r"\bwindows ml\b", r"\bnpu\b", r"\bedge\b",
        ],
        "description": "Windows for developers and agents — WSL Containers, Surface RTX Spark, Copilot+ PCs, on-device AI, Windows ML",
    },
    "Developer Tools": {
        "patterns": [
            r"\bvs ?code\b", r"\bgithub\b", r"\bcopilot cli\b",
            r"\bgithub copilot\b", r"\bauto fix\b", r"\bcodeql\b",
            r"\bazure devops\b", r"\bsdlc\b", r"\bopen source\b",
        ],
        "description": "GitHub + VS Code + GitHub Copilot — CLI, Copilot app, Auto Fix, Azure DevOps integration, agentic SDLC",
    },
    "Data + AI": {
        "patterns": [
            r"\bfabric\b", r"\bfabric iq\b", r"\bcosmos ?db\b",
            r"\bhorizondb\b", r"\bpostgres\b", r"\brayfin\b",
            r"\bsql\b", r"\bdatabricks\b", r"\bagentic retrieval\b",
            r"\bgrounding\b", r"\bvector\b", r"\brag\b",
        ],
        "description": "Data + AI platform — Fabric, Fabric IQ, Cosmos DB, Horizon DB (PostgreSQL), Rayfin, agentic retrieval, RAG",
    },
    "Microsoft IQ": {
        "patterns": [
            r"\bwork iq\b", r"\bweb iq\b", r"\bfoundry iq\b",
            r"\bfabric iq\b", r"\bmicrosoft iq\b",
        ],
        "description": "The Microsoft IQ family — Work IQ, Web IQ, Foundry IQ, Fabric IQ — context layers for the agentic web",
    },
    "Security + Governance": {
        "patterns": [
            r"\bagent 365\b", r"\bpurview\b", r"\bdefender\b",
            r"\bentra\b", r"\bintune\b", r"\bguardrail\b",
            r"\bresponsible ai\b", r"\bagent security\b", r"\bobservability\b",
            r"\bevaluation\b", r"\bsafety\b", r"\bred ?team",
        ],
        "description": "Agent governance and security — Agent 365, Purview, Defender, Entra, ASSERT, ACS, evaluation frameworks",
    },
    "Discovery + Frontier Science": {
        "patterns": [
            r"\bmicrosoft discovery\b", r"\bmajorana\b", r"\bquantum\b",
            r"\bfrontier r&?d\b", r"\bscientific\b", r"\bdrug discovery\b",
            r"\bmaterials science\b",
        ],
        "description": "Microsoft Discovery, Majorana 2 quantum chip, scientific R&D acceleration",
    },
    "M365 Copilot": {
        "patterns": [
            r"\bm365 copilot\b", r"\bmicrosoft 365 copilot\b",
            r"\bcopilot pages\b", r"\bcopilot chat\b", r"\bcopilot studio\b",
            r"\bcopilot credits\b", r"\bcopilot for\b",
        ],
        "description": "Microsoft 365 Copilot, Copilot Studio, Copilot Pages, Copilot Credits, vertical Copilots",
    },
}


def _stringify(v) -> str:
    if v is None:
        return ""
    if isinstance(v, list):
        return " ".join(_stringify(x) for x in v)
    return str(v)


def topic_for_session(session: dict) -> List[str]:
    """Return list of topic names that match a session."""
    text = " ".join([
        _stringify(session.get("title")),
        _stringify(session.get("description")),
        _stringify(session.get("aiSummary")),
        _stringify(session.get("topic")),
    ]).lower()
    matched = []
    for topic_name, cfg in TOPICS.items():
        for pat in cfg["patterns"]:
            if re.search(pat, text, re.IGNORECASE):
                matched.append(topic_name)
                break
    return matched


def list_topics() -> List[Dict[str, str]]:
    return [
        {"name": name, "description": cfg["description"]}
        for name, cfg in TOPICS.items()
    ]


def filter_sessions_by_topic(sessions: List[dict], topic_name: str) -> List[dict]:
    """Return sessions matching the given topic."""
    if topic_name not in TOPICS:
        return []
    cfg = TOPICS[topic_name]
    pats = [re.compile(p, re.IGNORECASE) for p in cfg["patterns"]]
    out = []
    for s in sessions:
        text = " ".join([
            _stringify(s.get("title")),
            _stringify(s.get("description")),
            _stringify(s.get("aiSummary")),
            _stringify(s.get("topic")),
        ])
        if any(p.search(text) for p in pats):
            out.append(s)
    return out


def detect_topic_in_query(query: str) -> List[str]:
    """If the query mentions a topic name, return matched topic names."""
    matched = []
    q_lower = query.lower()
    for topic_name, cfg in TOPICS.items():
        if topic_name.lower() in q_lower:
            matched.append(topic_name)
            continue
        # Also check if any pattern in the topic appears as a phrase in the query
        for pat in cfg["patterns"]:
            if re.search(pat, q_lower, re.IGNORECASE):
                if topic_name not in matched:
                    matched.append(topic_name)
                break
    return matched
