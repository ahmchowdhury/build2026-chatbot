"""CLI for the eval harness.

    python -m evals                                 # local, deterministic
    python -m evals --judge                         # add LLM judge
    python -m evals --url https://...               # against deployed app
    python -m evals --event build2026 --judge -k 3  # subset
    python -m evals --case naomi-prompt-caching     # one case
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .adapters import make_adapter
from .judge import Judge
from .report import compare_to_baseline, render_markdown, write_json, write_markdown
from .runner import load_event_config, load_gold, run_eval

REPO_ROOT = Path(__file__).parent.parent
EVAL_DIR = Path(__file__).parent


def main():
    parser = argparse.ArgumentParser(
        prog="python -m evals",
        description="RAG quality eval harness for the chatbot.",
    )
    parser.add_argument("--event", default="build2026",
                        help="event id (loads configs/<event>.yaml + gold/<event>.yaml)")
    parser.add_argument("--config", type=Path,
                        help="explicit event config YAML override")
    parser.add_argument("--gold", type=Path,
                        help="explicit gold YAML override")
    parser.add_argument("--url",
                        help="run against deployed HTTP endpoint instead of local")
    parser.add_argument("--judge", action="store_true",
                        help="run LLM-as-judge (requires AOAI env vars)")
    parser.add_argument("--case", action="append", default=[],
                        help="run only the specified case_id (repeatable)")
    parser.add_argument("--limit", type=int,
                        help="run only the first N cases")
    parser.add_argument("--tag", action="append", default=[],
                        help="run only cases tagged X (repeatable)")
    parser.add_argument("--report-dir", type=Path,
                        default=EVAL_DIR / "reports",
                        help="where to write report files")
    parser.add_argument("--baseline", type=Path,
                        help="compare to a previous report JSON")
    parser.add_argument("--strict", action="store_true",
                        help="exit non-zero if any case fails (CI gate)")
    parser.add_argument("--quiet", action="store_true",
                        help="suppress per-case progress, print summary only")
    args = parser.parse_args()

    # Resolve config + gold paths
    cfg_path = args.config or EVAL_DIR / "configs" / f"{args.event}.yaml"
    gold_path = args.gold or EVAL_DIR / "gold" / f"{args.event}.yaml"
    if not cfg_path.exists():
        print(f"event config not found: {cfg_path}", file=sys.stderr)
        sys.exit(2)
    if not gold_path.exists():
        print(f"gold dataset not found: {gold_path}", file=sys.stderr)
        sys.exit(2)

    cfg = load_event_config(cfg_path)
    gold = load_gold(gold_path)

    # Filter cases
    if args.case:
        gold = [c for c in gold if c.case_id in args.case]
        if not gold:
            print(f"No cases match --case {args.case}", file=sys.stderr)
            sys.exit(2)
    if args.tag:
        wanted = set(args.tag)
        gold = [c for c in gold if wanted & set(c.tags)]
    if args.limit:
        gold = gold[:args.limit]
    if not gold:
        print("No cases to run after filters.", file=sys.stderr)
        sys.exit(2)

    # Adapter + judge
    adapter = make_adapter(args.url)
    judge = Judge.from_env(cache_dir=EVAL_DIR / "cache") if args.judge else None
    if args.judge and not (judge and judge.available):
        print("--judge requested but AZURE_OPENAI_{ENDPOINT,KEY} not set; "
              "running deterministic only.", file=sys.stderr)

    print(f"Eval: event={cfg.event_id} target={'http' if args.url else 'local'} "
          f"cases={len(gold)} judge={'on' if (judge and judge.available) else 'off'}")
    print("")

    # Run
    dataset_version = _dataset_version(gold_path)
    target_label = "http" if args.url else "local"
    report = run_eval(
        cfg=cfg,
        gold=gold,
        adapter=adapter,
        judge=judge if (judge and judge.available) else None,
        dataset_id=f"{cfg.event_id}-gold",
        dataset_version=dataset_version,
        target_label=target_label,
    )

    # Write reports
    args.report_dir.mkdir(parents=True, exist_ok=True)
    ts = report.metadata.finished_at.replace(":", "").replace("-", "")
    base = args.report_dir / f"{cfg.event_id}-{target_label}-{ts}"
    write_json(report, base.with_suffix(".json"))
    write_markdown(report, base.with_suffix(".md"))
    print("")
    print(f"Report written: {base}.md  (and .json)")

    # Optional baseline diff
    if args.baseline:
        diff = compare_to_baseline(report, args.baseline)
        if diff:
            print("")
            print(diff)

    # Summary
    print("")
    print("=" * 60)
    print(f"Pass rate: {report.pass_rate:.0%} "
          f"({sum(1 for c in report.case_results if c.passed)}/"
          f"{len(report.case_results)})")
    if report.avg_groundedness is not None:
        print(f"Avg groundedness:    {report.avg_groundedness:.2f}")
        print(f"Avg attribution:     {report.avg_attribution_fidelity:.2f}")
    print("=" * 60)

    if args.strict and report.pass_rate < cfg.min_pass_rate:
        print(f"FAIL: pass_rate {report.pass_rate:.0%} < threshold "
              f"{cfg.min_pass_rate:.0%}", file=sys.stderr)
        sys.exit(1)
    if (args.strict and report.avg_groundedness is not None
            and report.avg_groundedness < cfg.min_groundedness):
        print(f"FAIL: groundedness {report.avg_groundedness:.2f} < threshold "
              f"{cfg.min_groundedness}", file=sys.stderr)
        sys.exit(1)


def _dataset_version(path: Path) -> str:
    """Use git short-SHA of the gold file as version, fall back to mtime."""
    import subprocess as sp
    try:
        sha = sp.check_output(
            ["git", "log", "-n1", "--format=%h", "--", str(path)],
            stderr=sp.DEVNULL,
        ).decode().strip()
        if sha:
            return sha
    except Exception:
        pass
    return f"mtime-{int(path.stat().st_mtime)}"


if __name__ == "__main__":
    main()
