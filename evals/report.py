"""Render a RunReport as JSON + Markdown."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

from .schema import RunReport


def write_json(report: RunReport, path: Path) -> None:
    path.write_text(report.model_dump_json(indent=2))


def render_markdown(report: RunReport) -> str:
    md = report.metadata
    out = []
    out.append(f"# RAG Eval Report — {md.event_id}")
    out.append("")
    out.append(f"**Run started:** {md.started_at}  ")
    out.append(f"**Duration:** {md.duration_s}s  ")
    out.append(f"**Target:** `{md.target}`  ")
    out.append(f"**Cases:** {md.case_count}  ")
    out.append(f"**Dataset:** {md.dataset_id} @ {md.dataset_version}  ")
    if md.git_sha:
        out.append(f"**git SHA:** `{md.git_sha}`  ")
    if md.search_index:
        out.append(f"**Search index:** `{md.search_index}`  ")
    if md.chat_model:
        out.append(f"**Chat model:** `{md.chat_model}` "
                   f"· **Embed:** `{md.embed_model}`  ")
    if md.judged:
        out.append(f"**Judge:** `{md.judge_model}`  ")
    out.append("")

    out.append("## Summary")
    out.append("")
    out.append("| Metric | Value |")
    out.append("| --- | --- |")
    passed = sum(1 for c in report.case_results if c.passed)
    failed = len(report.case_results) - passed
    out.append(f"| Pass rate | **{report.pass_rate:.0%}** "
               f"({passed}/{len(report.case_results)}) |")
    out.append(f"| Failures | {failed} |")
    if report.avg_groundedness is not None:
        out.append(f"| Avg groundedness | {report.avg_groundedness:.2f} |")
    if report.avg_attribution_fidelity is not None:
        out.append(f"| Avg attribution fidelity | "
                   f"{report.avg_attribution_fidelity:.2f} |")
    # latency stats
    lats = sorted(
        v.latency_ms for c in report.case_results
        for v in c.variants if v.latency_ms is not None
    )
    if lats:
        out.append(f"| Latency p50 | {lats[len(lats)//2]}ms |")
        out.append(f"| Latency p95 | {lats[min(int(len(lats)*0.95), len(lats)-1)]}ms |")
    out.append("")

    # Per-case breakdown
    out.append("## Cases")
    out.append("")
    out.append("| ✓ | Case | Expected | Variants | Failed checks |")
    out.append("| --- | --- | --- | --- | --- |")
    for c in report.case_results:
        emoji = "✅" if c.passed else "❌"
        failed_names = sorted({
            ch.name
            for v in c.variants for ch in v.checks if not ch.passed
        })
        out.append(
            f"| {emoji} | `{c.case_id}` | {c.expected_behavior} | "
            f"{len(c.variants)} | "
            f"{', '.join(failed_names) if failed_names else '—'} |"
        )
    out.append("")

    # Detailed failures
    failures = [c for c in report.case_results if not c.passed]
    if failures:
        out.append("## Failure Details")
        out.append("")
        for c in failures:
            out.append(f"### ❌ `{c.case_id}` — {c.description or ''}")
            out.append(f"_Expected behavior: `{c.expected_behavior}`_")
            out.append("")
            if c.error:
                out.append("```")
                out.append(c.error)
                out.append("```")
                continue
            for v in c.variants:
                if v.passed:
                    continue
                out.append(f"**Variant:** `{v.query}` "
                           f"(kind=`{v.kind}`, latency={v.latency_ms}ms)")
                for ch in v.checks:
                    if ch.passed:
                        continue
                    out.append(f"- ❌ **{ch.name}** — {ch.detail}")
                if v.judge:
                    j = v.judge
                    out.append(f"- 🧑‍⚖️ judge: G={j.groundedness:.2f} "
                               f"A={j.attribution_fidelity:.2f} "
                               f"R={j.answer_relevance:.2f}  ")
                    out.append(f"  > {j.rationale}")
                    if j.unsupported_claims:
                        out.append(f"  unsupported: {j.unsupported_claims}")
                out.append(f"<details><summary>Answer (truncated)</summary>\n\n```\n"
                           f"{(v.answer or '')[:1500]}\n```\n</details>")
                out.append("")

    # Pass-but-judged details
    judged_cases = [c for c in report.case_results
                    if c.passed and any(v.judge for v in c.variants)]
    if judged_cases:
        out.append("## Judged Cases (passing)")
        out.append("")
        out.append("| Case | Groundedness | Attribution | Relevance | Cached |")
        out.append("| --- | --- | --- | --- | --- |")
        for c in judged_cases:
            v = next((v for v in c.variants if v.judge), None)
            if not v or not v.judge:
                continue
            j = v.judge
            out.append(
                f"| `{c.case_id}` | {j.groundedness:.2f} | "
                f"{j.attribution_fidelity:.2f} | "
                f"{j.answer_relevance:.2f} | "
                f"{'✓' if j.cached else '·'} |"
            )
        out.append("")

    return "\n".join(out)


def write_markdown(report: RunReport, path: Path) -> None:
    path.write_text(render_markdown(report))


def compare_to_baseline(current: RunReport,
                        baseline_path: Path) -> Optional[str]:
    """If a baseline JSON report exists, produce a brief markdown diff
    showing regressions.
    """
    if not baseline_path.exists():
        return None
    try:
        baseline = RunReport(**json.loads(baseline_path.read_text()))
    except Exception as e:
        return f"_Could not load baseline ({e})_"
    diffs = []
    bp = baseline.pass_rate
    cp = current.pass_rate
    delta = cp - bp
    diffs.append(f"## Regression vs baseline ({baseline.metadata.git_sha or '?'})")
    diffs.append(f"- pass_rate: {bp:.0%} → {cp:.0%} ({'+' if delta >= 0 else ''}{delta:.0%})")
    if baseline.avg_groundedness and current.avg_groundedness:
        bg = baseline.avg_groundedness
        cg = current.avg_groundedness
        diffs.append(f"- groundedness: {bg:.2f} → {cg:.2f} ({'+' if cg-bg >= 0 else ''}{cg-bg:.2f})")
    # case-level regressions
    base_results = {c.case_id: c.passed for c in baseline.case_results}
    regressions = [c.case_id for c in current.case_results
                   if c.case_id in base_results
                   and base_results[c.case_id] and not c.passed]
    new_passes = [c.case_id for c in current.case_results
                  if c.case_id in base_results
                  and not base_results[c.case_id] and c.passed]
    if regressions:
        diffs.append(f"- **Regressed cases ({len(regressions)}):** "
                     + ", ".join(f"`{r}`" for r in regressions))
    if new_passes:
        diffs.append(f"- **Newly passing ({len(new_passes)}):** "
                     + ", ".join(f"`{r}`" for r in new_passes))
    return "\n".join(diffs)
