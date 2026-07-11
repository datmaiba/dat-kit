#!/usr/bin/env python3
"""dat-kit scorecard aggregator.

Fills real token usage into benchmarks/scorecard.jsonl (written by the
scorecard skill) by parsing Claude Code transcript files, then prints an
aggregate benchmark table.

Usage (from the project you want to report on):
    python3 /path/to/dat-kit/scripts/scorecard.py            # fill tokens + report
    python3 .../scorecard.py --report-only                   # just the table
    python3 .../scorecard.py --projects-dir /custom/path     # override transcript location (tests)

Token matching: each scorecard entry's `ts` is matched to the transcript
session whose [first, last] message window contains it (or ends within 6h
before it). Unmatched entries keep tokens=null — they are listed, never guessed.
"""
import argparse, json, os, pathlib, re, sys
from datetime import datetime, timedelta, timezone


def parse_ts(s):
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except Exception:
        return None


def project_transcript_dir(projects_dir: pathlib.Path, cwd: str) -> pathlib.Path:
    return projects_dir / re.sub(r"[^A-Za-z0-9-]", "-", cwd)


def scan_sessions(tdir: pathlib.Path):
    """Yield (session_id, first_ts, last_ts, tokens_dict) per transcript file.
    Defensive: transcript format is Claude Code internal — we walk every JSON
    line and sum any dict literally named 'usage' with known token keys."""
    KEYS = ("input_tokens", "output_tokens", "cache_creation_input_tokens", "cache_read_input_tokens")
    for f in sorted(tdir.glob("*.jsonl")):
        first = last = None
        totals = dict.fromkeys(KEYS, 0)

        def walk(node):
            if isinstance(node, dict):
                for k, v in node.items():
                    if k == "usage" and isinstance(v, dict):
                        for kk in KEYS:
                            if isinstance(v.get(kk), int):
                                totals[kk] += v[kk]
                    else:
                        walk(v)
            elif isinstance(node, list):
                for x in node:
                    walk(x)

        for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                obj = json.loads(line)
            except Exception:
                continue
            ts = parse_ts(obj.get("timestamp", "")) if isinstance(obj, dict) else None
            if ts:
                first = first or ts
                last = ts
            walk(obj)
        if any(totals.values()):
            yield f.stem, first, last, totals


def fill_tokens(entries, sessions):
    filled = 0
    for e in entries:
        if e.get("tokens") is not None:
            continue
        ts = parse_ts(e.get("ts", "") or "")
        if not ts:
            continue
        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=timezone.utc)
        for sid, first, last, tot in sessions:
            if not (first and last):
                continue
            lo = first - timedelta(minutes=5)
            hi = last + timedelta(hours=6)
            if lo <= ts <= hi:
                e["tokens"] = {**tot, "total": sum(tot.values()), "session": sid[:8]}
                filled += 1
                break
    return filled


def report(entries):
    if not entries:
        print("No scorecard entries yet — the scorecard skill writes benchmarks/scorecard.jsonl")
        return
    W = (12, 34, 4, 7, 8, 10)
    print(f"{'date':<{W[0]}} {'task':<{W[1]}} {'cx':<{W[2]}} {'est.h':<{W[3]}} {'wall.m':<{W[4]}} {'tokens':<{W[5]}}")
    tot_h = tot_m = tot_t = 0
    cx_sum = 0.0
    for e in entries:
        t = e.get("tokens") or {}
        tok = t.get("total")
        print(f"{e.get('date',''):<{W[0]}} {e.get('task','')[:W[1]]:<{W[1]}} "
              f"{e.get('complexity','?'):<{W[2]}} {e.get('est_manual_hours','?'):<{W[3]}} "
              f"{e.get('actual_wall_minutes','?'):<{W[4]}} {tok if tok else '—':<{W[5]}}")
        tot_h += float(e.get("est_manual_hours") or 0)
        tot_m += float(e.get("actual_wall_minutes") or 0)
        tot_t += tok or 0
        cx_sum += float(e.get("complexity") or 0)
    n = len(entries)
    print("-" * 80)
    print(f"{n} tasks | complexity avg {cx_sum/n:.1f} | est. manual hours (ESTIMATE): {tot_h:.1f} "
          f"| actual: {tot_m/60:.1f}h | tokens: {tot_t:,}")
    if tot_t and cx_sum:
        print(f"tokens per complexity-point: {tot_t/cx_sum:,.0f} | est. hours saved (ESTIMATE): {tot_h - tot_m/60:.1f}")
    print("Note: 'hours saved' compares an ESTIMATED manual baseline with real wall time — treat as directional, not exact.")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--projects-dir", default=os.path.expanduser("~/.claude/projects"))
    ap.add_argument("--project", default=os.getcwd(), help="project path whose transcripts to scan")
    ap.add_argument("--report-only", action="store_true")
    args = ap.parse_args()

    sc_path = pathlib.Path(args.project) / "benchmarks" / "scorecard.jsonl"
    entries = []
    if sc_path.exists():
        entries = [json.loads(x) for x in sc_path.read_text().splitlines() if x.strip()]

    if not args.report_only:
        tdir = project_transcript_dir(pathlib.Path(args.projects_dir), args.project)
        if tdir.is_dir():
            n = fill_tokens(entries, list(scan_sessions(tdir)))
            if n:
                sc_path.write_text("".join(json.dumps(e, ensure_ascii=False) + "\n" for e in entries))
                print(f"filled tokens for {n} entr{'y' if n==1 else 'ies'} from {tdir}\n")
        else:
            print(f"(no transcripts found at {tdir} — tokens stay null; is this the right machine/project?)\n")

    report(entries)


if __name__ == "__main__":
    main()
