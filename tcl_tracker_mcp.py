#!/usr/bin/env python3
"""TCL Electronics KSA — Training Tracker MCP Server

Exposes the training system as MCP tools so Claude (or any MCP client)
can automate promoter tracking, quizzes, leaderboard, competitions,
and Excel report generation via natural language.

Run:
    python tcl_tracker_mcp.py

Add to Claude Code ~/.claude/claude.json:
    {
      "mcpServers": {
        "tcl-training": {
          "command": "python",
          "args": ["/path/to/greet/tcl_tracker_mcp.py"]
        }
      }
    }
"""

import json
from datetime import date
from pathlib import Path

from mcp.server.fastmcp import FastMCP

# ── Re-use data layer from tcl_training.py ────────────────────────────────────
DATA_FILE = Path(__file__).parent / "tcl_training_data.json"
PLAN_FILE = Path(__file__).parent / "training_data.json"
TODAY     = date.today().isoformat()

POINTS_MAP = {
    "quiz_bronze": 10, "quiz_silver": 20, "quiz_gold": 35,
    "quiz_perfect_bonus": 5,
    "comp_submit": 15, "comp_1st": 25, "comp_2nd": 15, "comp_3rd": 10,
}
LEVELS       = [(150, "Champion"), (100, "Gold"), (50, "Silver"), (0, "Bronze")]
LEVEL_BADGES = {"Champion": "🏆", "Gold": "🥇", "Silver": "🥈", "Bronze": "🥉"}
RUBRIC       = {"knowledge": 0.35, "creativity": 0.25, "selling": 0.40}


def _load() -> dict:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {"promoters": {}, "competitions": {}}


def _save(data: dict) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2))


def _get_level(pts: int) -> str:
    for threshold, name in LEVELS:
        if pts >= threshold:
            return name
    return "Bronze"


def _add_points(p: dict, pts: int, reason: str) -> None:
    p["points"] = p.get("points", 0) + pts
    p["level"]  = _get_level(p["points"])
    p.setdefault("history", []).append({"date": TODAY, "pts": pts, "reason": reason})


def _next_id(data: dict) -> str:
    existing = [int(k[1:]) for k in data["promoters"] if k.startswith("P")]
    return f"P{(max(existing) + 1 if existing else 1):03d}"


# ── MCP server ────────────────────────────────────────────────────────────────
mcp = FastMCP("TCL Training Tracker")


# ─── Promoter tools ───────────────────────────────────────────────────────────

@mcp.tool()
def add_promoter(name: str, store: str) -> str:
    """Register a new promoter. Returns their assigned ID."""
    data = _load()
    pid  = _next_id(data)
    data["promoters"][pid] = {
        "id": pid, "name": name, "store": store,
        "joined": TODAY, "points": 0, "level": "Bronze",
        "quiz_results": [], "comp_entries": [], "history": [],
    }
    _save(data)
    return f"Registered: {pid} — {name} ({store})"


@mcp.tool()
def list_promoters() -> str:
    """List all registered promoters with their points and level."""
    data = _load()
    ps   = sorted(data["promoters"].values(), key=lambda x: x["points"], reverse=True)
    if not ps:
        return "No promoters registered yet."
    lines = ["ID     Name                   Store                 Pts   Level"]
    lines.append("─" * 65)
    for p in ps:
        badge = LEVEL_BADGES[p["level"]]
        lines.append(f"{p['id']:<6} {p['name']:<22} {p['store']:<22} {p['points']:>4}  {badge} {p['level']}")
    return "\n".join(lines)


@mcp.tool()
def get_promoter_profile(promoter_id: str) -> str:
    """Get full profile, quiz history, and points log for a promoter."""
    data = _load()
    p    = data["promoters"].get(promoter_id.upper())
    if not p:
        return f"Promoter '{promoter_id}' not found."
    lines = [
        f"ID:     {p['id']}",
        f"Name:   {p['name']}",
        f"Store:  {p['store']}",
        f"Points: {p['points']}  |  Level: {LEVEL_BADGES[p['level']]} {p['level']}",
    ]
    if p["quiz_results"]:
        lines.append("\nQuiz Results:")
        for r in p["quiz_results"]:
            lines.append(f"  {r['quiz']:16} {r['score']}/{r['total']} ({r['pct']}%) {'PASS' if r['passed'] else 'FAIL'}  {r['date']}")
    if p["comp_entries"]:
        lines.append("\nCompetition Entries:")
        for e in p["comp_entries"]:
            lines.append(f"  {e['comp']}  Score: {e['weighted_score']:.3f}  Rank: {e.get('rank','–')}  {e['date']}")
    if p["history"]:
        lines.append("\nPoints History (last 10):")
        for h in p["history"][-10:]:
            lines.append(f"  {h['date']}  +{h['pts']} pts  —  {h['reason']}")
    return "\n".join(lines)


# ─── Quiz tools ───────────────────────────────────────────────────────────────

@mcp.tool()
def list_quizzes() -> str:
    """List all available quizzes with their level and pass threshold."""
    from tcl_training import QUIZ_BANK
    lines = ["ID               Name                        Level   Qs  Pass%"]
    lines.append("─" * 60)
    for qid, q in QUIZ_BANK.items():
        lines.append(f"{qid:<16} {q['name']:<28} {q['level']:<8} {len(q['questions']):<4} {q['pass_pct']}%")
    return "\n".join(lines)


@mcp.tool()
def score_quiz(promoter_id: str, quiz_id: str, answers: list[str]) -> str:
    """
    Score a completed quiz for a promoter without interactive prompts.
    Pass answers as a list of single letters e.g. ["A","C","B","A",...].
    Returns score, pass/fail status, and points awarded.
    """
    from tcl_training import QUIZ_BANK
    data = _load()
    p    = data["promoters"].get(promoter_id.upper())
    if not p:
        return f"Promoter '{promoter_id}' not found."
    quiz = QUIZ_BANK.get(quiz_id)
    if not quiz:
        return f"Quiz '{quiz_id}' not found."
    questions = quiz["questions"]
    if len(answers) != len(questions):
        return f"Expected {len(questions)} answers, got {len(answers)}."

    score = 0
    total = sum(q["pts"] for q in questions)
    details = []
    for i, (q, ans) in enumerate(zip(questions, answers), 1):
        correct = ans.upper() == q["answer"]
        if correct:
            score += q["pts"]
        details.append(f"Q{i}: {'✓' if correct else '✗'}  (correct: {q['answer']})")

    pct    = int(score / total * 100)
    passed = pct >= quiz["pass_pct"]

    pts_earned = 0
    if passed:
        pts_earned += POINTS_MAP.get(f"quiz_{quiz['level']}", 10)
        _add_points(p, pts_earned, f"{quiz['name']} pass")
        if pct == 100:
            bonus = POINTS_MAP["quiz_perfect_bonus"]
            pts_earned += bonus
            _add_points(p, bonus, f"{quiz['name']} perfect score bonus")

    p["quiz_results"].append({
        "quiz": quiz_id, "score": score, "total": total,
        "pct": pct, "passed": passed, "date": TODAY,
    })
    _save(data)

    result = [
        f"Quiz: {quiz['name']}  |  Promoter: {p['name']}",
        f"Score: {score}/{total} ({pct}%)  |  {'PASSED ✓' if passed else 'FAILED ✗'}",
        f"Points awarded: +{pts_earned}  |  New total: {p['points']} ({p['level']})",
        "",
    ] + details
    return "\n".join(result)


@mcp.tool()
def get_quiz_questions(quiz_id: str) -> str:
    """Return all questions for a quiz (without revealing answers) so you can present them to a promoter."""
    from tcl_training import QUIZ_BANK
    quiz = QUIZ_BANK.get(quiz_id)
    if not quiz:
        return f"Quiz '{quiz_id}' not found."
    lines = [f"{quiz['name']}  |  {len(quiz['questions'])} questions  |  Pass: {quiz['pass_pct']}%", ""]
    for i, q in enumerate(quiz["questions"], 1):
        lines.append(f"Q{i}. {q['q']}")
        for opt in q["options"]:
            lines.append(f"    {opt}")
        lines.append("")
    return "\n".join(lines)


# ─── Leaderboard tool ─────────────────────────────────────────────────────────

@mcp.tool()
def get_leaderboard() -> str:
    """Return the current promoter leaderboard ranked by points."""
    data = _load()
    ps   = sorted(data["promoters"].values(), key=lambda x: x["points"], reverse=True)
    if not ps:
        return "No promoters yet."
    month = date.today().strftime("%B %Y")
    lines = [f"TCL PROMOTER LEADERBOARD — {month}", "═" * 60]
    lines.append(f"{'#':<5} {'Name':<22} {'Store':<22} {'Pts':>5}  Level")
    for i, p in enumerate(ps, 1):
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"{i}.")
        badge = LEVEL_BADGES[p["level"]]
        lines.append(f"{medal:<5} {p['name']:<22} {p['store']:<22} {p['points']:>5}  {badge} {p['level']}")
    lines.append("")
    above = sum(1 for p in ps if p["level"] != "Bronze")
    lines.append(f"Leader: {ps[0]['name']} with {ps[0]['points']} pts")
    lines.append(f"Above Bronze: {above}/{len(ps)} promoters")
    return "\n".join(lines)


# ─── Competition tools ────────────────────────────────────────────────────────

@mcp.tool()
def create_competition(name: str) -> str:
    """Create a new competition. Returns the competition ID."""
    data     = _load()
    existing = [int(k[1:]) for k in data["competitions"] if k.startswith("C")]
    cid      = f"C{(max(existing) + 1 if existing else 1):03d}"
    data["competitions"][cid] = {
        "id": cid, "name": name, "date": TODAY, "entries": [], "ranked": False,
    }
    _save(data)
    return f"Competition created: {cid} — {name}"


@mcp.tool()
def score_competition_entry(
    competition_id: str,
    promoter_id: str,
    knowledge_score: int,
    creativity_score: int,
    selling_score: int,
) -> str:
    """
    Score a promoter's competition entry using the rubric.
    knowledge_score, creativity_score, selling_score must each be 1–4.
    Returns weighted score and points awarded.
    """
    data = _load()
    cid  = competition_id.upper()
    pid  = promoter_id.upper()
    comp = data["competitions"].get(cid)
    if not comp:
        return f"Competition '{cid}' not found."
    p = data["promoters"].get(pid)
    if not p:
        return f"Promoter '{pid}' not found."
    if any(e["promoter_id"] == pid for e in comp["entries"]):
        return f"{p['name']} already has an entry in this competition."
    for val, name in [(knowledge_score,"knowledge"),(creativity_score,"creativity"),(selling_score,"selling")]:
        if val not in (1, 2, 3, 4):
            return f"{name} score must be 1–4, got {val}."

    scores   = {"knowledge": knowledge_score, "creativity": creativity_score, "selling": selling_score}
    weighted = sum(scores[k] * RUBRIC[k] for k in scores)
    pct      = int(weighted / 4 * 100)

    comp["entries"].append({
        "promoter_id": pid, "promoter_name": p["name"], "store": p["store"],
        "scores": scores, "weighted_score": round(weighted, 3), "pct": pct, "date": TODAY,
    })
    _add_points(p, POINTS_MAP["comp_submit"], f"Submitted to {comp['name']}")
    p["comp_entries"].append({"comp": cid, "weighted_score": round(weighted, 3), "date": TODAY})
    _save(data)

    return (
        f"Entry saved for {p['name']} in {comp['name']}\n"
        f"Score: {weighted:.3f}/4.00 ({pct}%)\n"
        f"Submission points: +{POINTS_MAP['comp_submit']}  |  New total: {p['points']} ({p['level']})"
    )


@mcp.tool()
def finalize_competition(competition_id: str) -> str:
    """Rank all entries, distribute award points to top 3, and return final standings."""
    data = _load()
    cid  = competition_id.upper()
    comp = data["competitions"].get(cid)
    if not comp:
        return f"Competition '{cid}' not found."
    if not comp["entries"]:
        return "No entries to rank."

    ranked    = sorted(comp["entries"], key=lambda e: e["weighted_score"], reverse=True)
    award_pts = {1: POINTS_MAP["comp_1st"], 2: POINTS_MAP["comp_2nd"], 3: POINTS_MAP["comp_3rd"]}
    award_sar = {1: "1,000 SAR 🥇", 2: "800 SAR 🥈", 3: "600 SAR 🥉"}
    lines     = [f"FINAL RANKINGS — {comp['name']}", "─" * 55]

    for i, entry in enumerate(ranked, 1):
        medal = {1: "🥇 1st", 2: "🥈 2nd", 3: "🥉 3rd"}.get(i, f"  {i}th")
        lines.append(f"{medal:<8} {entry['promoter_name']:<22} {entry['weighted_score']:.3f}/4.00 ({entry['pct']}%)")
        e_ref = next(e for e in comp["entries"] if e["promoter_id"] == entry["promoter_id"])
        if "rank" not in e_ref:
            e_ref["rank"] = i
            if i <= 3:
                p = data["promoters"].get(entry["promoter_id"])
                if p:
                    _add_points(p, award_pts[i], f"{comp['name']} rank #{i}")
                    pe = next((x for x in p["comp_entries"] if x["comp"] == cid), None)
                    if pe:
                        pe["rank"] = i

    comp["ranked"] = True
    _save(data)
    lines.append("\nAwards:")
    for i, entry in enumerate(ranked[:3], 1):
        lines.append(f"  {entry['promoter_name']:<22} {award_sar[i]}")
    return "\n".join(lines)


@mcp.tool()
def get_competition_results(competition_id: str) -> str:
    """Return the full results table for a competition."""
    data = _load()
    cid  = competition_id.upper()
    comp = data["competitions"].get(cid)
    if not comp:
        return f"Competition '{cid}' not found."
    if not comp["entries"]:
        return "No entries yet."
    ranked = sorted(comp["entries"], key=lambda e: e["weighted_score"], reverse=True)
    lines  = [f"{comp['name']}  |  {comp['date']}  |  {len(ranked)} entries",
              "Rubric: Knowledge 35%  ·  Creativity 25%  ·  Selling 40%", ""]
    lines.append(f"{'#':<4} {'Promoter':<22} {'Knwl':>5} {'Crtv':>5} {'Sell':>5} {'Score':>7}  {'%':>5}")
    lines.append("─" * 55)
    for i, e in enumerate(ranked, 1):
        s = e["scores"]
        lines.append(f"{i:<4} {e['promoter_name']:<22} {s['knowledge']:>5} {s['creativity']:>5} {s['selling']:>5} {e['weighted_score']:>7.3f}  {e['pct']:>4}%")
    return "\n".join(lines)


# ─── Training plan tools ──────────────────────────────────────────────────────

@mcp.tool()
def get_training_plan() -> str:
    """Return the June 2026 monthly training plan with task statuses."""
    if not PLAN_FILE.exists():
        return "No training plan found."
    plan  = json.loads(PLAN_FILE.read_text())
    tasks = [t for w in plan["weeks"] for t in w["tasks"]]
    done  = sum(1 for t in tasks if t["status"] == "done")
    total = len(tasks)
    lines = [f"Training Plan — {plan['month']}",
             f"Progress: {done}/{total} ({int(done/total*100)}%)", ""]
    icons = {"done": "[x]", "todo": "[ ]", "skip": "[-]"}
    for week in plan["weeks"]:
        lines.append(f"Week {week['week']}: {week['label']}")
        for t in week["tasks"]:
            lines.append(f"  {icons[t['status']]} {t['id']:5}  {t['day']:12}  {t['name']}")
        lines.append("")
    return "\n".join(lines)


@mcp.tool()
def update_training_task(task_id: str, status: str) -> str:
    """
    Update a training task status.
    status must be one of: done, todo, skip
    task_id examples: w1d1, w2d3, w4d5
    """
    if status not in ("done", "todo", "skip"):
        return "status must be: done, todo, or skip"
    if not PLAN_FILE.exists():
        return "No training plan found."
    plan  = json.loads(PLAN_FILE.read_text())
    tasks = [t for w in plan["weeks"] for t in w["tasks"]]
    task  = next((t for t in tasks if t["id"] == task_id), None)
    if not task:
        return f"Task '{task_id}' not found."
    old = task["status"]
    task["status"] = status
    PLAN_FILE.write_text(json.dumps(plan, indent=2))
    return f"Task {task_id} updated: {old} → {status}  ({task['name']})"


# ─── Report tool ──────────────────────────────────────────────────────────────

@mcp.tool()
def generate_report(format: str = "text") -> str:
    """
    Generate a training summary report.
    format: 'text' for plain text, 'excel' to produce an .xlsx file.
    Returns a summary or the file path of the generated Excel report.
    """
    if format == "excel":
        import subprocess, sys
        result = subprocess.run(
            [sys.executable, str(Path(__file__).parent / "tcl_report_excel.py")],
            capture_output=True, text=True
        )
        return result.stdout.strip() or result.stderr.strip()

    data = _load()
    ps   = sorted(data["promoters"].values(), key=lambda x: x["points"], reverse=True)
    if not ps:
        return "No data yet."

    total   = len(ps)
    avg_pts = sum(p["points"] for p in ps) / total
    levels  = {}
    for p in ps:
        levels[p["level"]] = levels.get(p["level"], 0) + 1

    lines = [
        f"TCL TRAINING REPORT — {date.today().strftime('%B %Y')}",
        "═" * 55,
        f"Promoters: {total}  |  Avg points: {avg_pts:.1f}  |  Competitions: {len(data['competitions'])}",
        "",
        "Level Breakdown:",
    ]
    for lvl, cnt in levels.items():
        lines.append(f"  {LEVEL_BADGES[lvl]} {lvl:<10} {cnt}")

    lines += ["", "Leaderboard:"]
    for i, p in enumerate(ps, 1):
        lines.append(f"  {i}. {p['name']:<22} {p['points']:>4} pts  {p['level']}")

    quiz_attempts = sum(len(p.get("quiz_results", [])) for p in ps)
    quiz_passed   = sum(sum(1 for r in p.get("quiz_results", []) if r["passed"]) for p in ps)
    lines += [
        "", f"Quizzes: {quiz_attempts} attempted, {quiz_passed} passed",
        "", "Recommended Actions:",
    ]
    no_quiz = [p["name"] for p in ps if not p.get("quiz_results")]
    if no_quiz:
        lines.append(f"  • Needs first quiz: {', '.join(no_quiz)}")
    close = [p for p in ps if p["level"] == "Bronze" and p["points"] >= 40]
    if close:
        lines.append(f"  • Close to Silver: {', '.join(p['name'] for p in close)}")
    return "\n".join(lines)


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    mcp.run()
