"""Orchestrates a full eval run. Loads cases, calls adapter, runs metrics,
optionally runs the LLM judge, returns a `RunReport`.

Failure semantics:
  * A `case` is one logical assertion ("Naomi prompt caching returns BRK230").
  * A `case` has 1 canonical query + N optional variants.
  * EVERY variant runs through ALL deterministic checks.
  * Judge runs once per case on the canonical query (cost control).
  * Case passes iff all variants pass all checks AND, when judge ran,
    groundedness >= cfg.min_groundedness.
"""
from __future__ import annotations

import datetime as dt
import os
import subprocess
import time
import traceback
from pathlib import Path
from typing import List, Optional

import yaml

from .adapters import Adapter, make_adapter
from .judge import Judge
from .metrics import run_all_checks
from .schema import (CaseResult, CheckResult, EventConfig, GoldCase,
                     RunMetadata, RunReport, VariantOutcome)


def _git_sha() -> Optional[str]:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--short", "HEAD"],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except Exception:
        return None


def load_event_config(path: Path) -> EventConfig:
    data = yaml.safe_load(path.read_text())
    return EventConfig(**data)


def load_gold(path: Path) -> List[GoldCase]:
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, list):
        raise ValueError(f"gold file {path} must be a YAML list of cases")
    return [GoldCase(**c) for c in data]


def evaluate_case(
    case: GoldCase,
    adapter: Adapter,
    cfg: EventConfig,
    judge: Optional[Judge],
    target: str,
) -> CaseResult:
    """Run one case through every variant + all checks + (optional) judge."""
    queries = [case.query] + list(case.query_variants)
    variants: List[VariantOutcome] = []
    judge_done = False
    for i, q in enumerate(queries):
        try:
            out = adapter.ask(q)
        except Exception as e:
            checks = [CheckResult(
                name="adapter_call",
                passed=False,
                detail=f"adapter raised: {e!r}",
            )]
            variants.append(VariantOutcome(
                query=q, answer="", kind="error",
                session_codes=[], latency_ms=None, checks=checks,
            ))
            continue

        # Canonical query gets the substring constraints; variants only get
        # the structural / retrieval / refusal checks to avoid over-fitting
        # wording.
        effective_case = case if i == 0 else case.model_copy(update={
            "must_contain_all": [],
            "required_citations": [],
        })
        checks = run_all_checks(out, effective_case, cfg, target=target)
        variant = VariantOutcome(
            query=q,
            answer=out.get("answer", ""),
            kind=out.get("kind", ""),
            session_codes=list(out.get("session_codes") or []),
            latency_ms=out.get("_latency_ms_observed"),
            checks=checks,
        )

        # Run the LLM judge once per case, on the canonical variant only
        if (judge and judge.available and i == 0
                and not case.skip_judge and not judge_done):
            passages = (out.get("eval_trace") or {}).get("retrieved") or []
            try:
                variant.judge = judge.judge(case, variant.answer, passages)
            except Exception as e:
                variant.judge = None
                variant.checks.append(CheckResult(
                    name="judge_error", passed=False,
                    detail=f"judge raised: {e!r}",
                ))
            judge_done = True
            # Promote groundedness to a hard check.
            if variant.judge:
                g = variant.judge.groundedness
                a = variant.judge.attribution_fidelity
                variant.checks.append(CheckResult(
                    name="judge_groundedness",
                    passed=g >= cfg.min_groundedness,
                    score=g,
                    detail=f"groundedness={g:.2f} threshold={cfg.min_groundedness}",
                ))
                variant.checks.append(CheckResult(
                    name="judge_attribution",
                    passed=a >= cfg.min_attribution_fidelity,
                    score=a,
                    detail=f"attribution_fidelity={a:.2f} threshold={cfg.min_attribution_fidelity}",
                ))
        variants.append(variant)

    return CaseResult(
        case_id=case.case_id,
        description=case.description,
        expected_behavior=case.expected_behavior.value,
        variants=variants,
    )


def run_eval(
    cfg: EventConfig,
    gold: List[GoldCase],
    adapter: Adapter,
    judge: Optional[Judge] = None,
    dataset_id: str = "default",
    dataset_version: str = "unknown",
    target_label: str = "local",
) -> RunReport:
    started = dt.datetime.utcnow()
    t0 = time.perf_counter()
    case_results: List[CaseResult] = []
    for i, case in enumerate(gold, 1):
        print(f"  [{i:2d}/{len(gold)}] {case.case_id:<45s} ", end="", flush=True)
        try:
            res = evaluate_case(case, adapter, cfg, judge, target_label)
        except Exception as e:
            res = CaseResult(
                case_id=case.case_id,
                description=case.description,
                expected_behavior=case.expected_behavior.value,
                variants=[],
                error=f"{e!r}\n{traceback.format_exc()[:400]}",
            )
        if res.passed:
            print("PASS")
        else:
            failed_names = [
                c.name for v in res.variants for c in v.checks if not c.passed
            ] or ["(no checks)"]
            print(f"FAIL [{','.join(failed_names[:4])}]"
                  + ("..." if len(failed_names) > 4 else ""))
        case_results.append(res)

    finished = dt.datetime.utcnow()
    duration = time.perf_counter() - t0
    metadata = RunMetadata(
        started_at=started.isoformat(timespec="seconds") + "Z",
        finished_at=finished.isoformat(timespec="seconds") + "Z",
        duration_s=round(duration, 2),
        event_id=cfg.event_id,
        dataset_id=dataset_id,
        dataset_version=dataset_version,
        target=target_label,
        git_sha=_git_sha(),
        search_index=os.environ.get("AZURE_SEARCH_INDEX"),
        chat_model=os.environ.get("AZURE_OPENAI_CHAT_DEPLOYMENT"),
        embed_model=os.environ.get("AZURE_OPENAI_EMBED_DEPLOYMENT"),
        judge_model=judge.model_id if (judge and judge.available) else None,
        judged=bool(judge and judge.available),
        case_count=len(gold),
    )
    return RunReport(metadata=metadata, case_results=case_results)
