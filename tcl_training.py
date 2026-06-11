#!/usr/bin/env python3
"""TCL Electronics KSA — Promoter Training System
   Tools: Quiz Runner · Promoter Tracker · Leaderboard · Competition Scorer
"""

import json
import sys
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).parent / "tcl_training_data.json"
TODAY = date.today().isoformat()

# ── Points config ────────────────────────────────────────────────────────────
POINTS_MAP = {
    "quiz_bronze": 10,
    "quiz_silver": 20,
    "quiz_gold":   35,
    "quiz_perfect_bonus": 5,
    "comp_submit": 15,
    "comp_1st":    25,
    "comp_2nd":    15,
    "comp_3rd":    10,
    "coaching":    10,
}

LEVELS = [(150, "Champion"), (100, "Gold"), (50, "Silver"), (0, "Bronze")]
LEVEL_BADGES = {"Champion": "🏆", "Gold": "🥇", "Silver": "🥈", "Bronze": "🥉"}

# Competition rubric weights (must sum to 1.0)
RUBRIC = {"knowledge": 0.35, "creativity": 0.25, "selling": 0.40}

# ── Built-in quiz bank ───────────────────────────────────────────────────────
QUIZ_BANK = {
    "c7l_bronze": {
        "name": "C7L Bronze Quiz",
        "product": "TCL C7L",
        "level": "bronze",
        "pass_pct": 70,
        "questions": [
            {
                "q": "What panel technology does the TCL C7L use?",
                "options": ["A) QLED", "B) Mini-LED", "C) OLED", "D) VA"],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "What is the maximum refresh rate of the TCL C7L?",
                "options": ["A) 60 Hz", "B) 90 Hz", "C) 120 Hz", "D) 144 Hz"],
                "answer": "C",
                "pts": 1,
            },
            {
                "q": "Which smart TV operating system does the C7L run?",
                "options": ["A) Tizen", "B) webOS", "C) Google TV", "D) Android TV"],
                "answer": "C",
                "pts": 1,
            },
            {
                "q": "Which gaming feature does the C7L support?",
                "options": ["A) VRR (Variable Refresh Rate)", "B) No gaming mode", "C) 30 Hz only", "D) G-Sync exclusive"],
                "answer": "A",
                "pts": 1,
            },
            {
                "q": "How many HDMI 2.1 ports does the C7L have?",
                "options": ["A) 0", "B) 1", "C) 2", "D) 4"],
                "answer": "C",
                "pts": 1,
            },
            {
                "q": "What is the main advantage of Mini-LED over standard LED?",
                "options": [
                    "A) Cheaper to produce",
                    "B) Better local dimming and contrast",
                    "C) Thinner panel",
                    "D) Lower power consumption only",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "Which audio technology does the C7L support for immersive sound?",
                "options": ["A) Dolby Atmos", "B) DTS only", "C) Stereo only", "D) PCM only"],
                "answer": "A",
                "pts": 1,
            },
            {
                "q": "The C7L is part of TCL's which product tier?",
                "options": ["A) Entry-level", "B) Mid-range premium", "C) Ultra-flagship", "D) Commercial display"],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "TCL is the official partner of which global event?",
                "options": ["A) FIFA World Cup", "B) Formula 1", "C) Olympic Games", "D) NBA Finals"],
                "answer": "C",
                "pts": 1,
            },
            {
                "q": "A customer says the C7L price is too high vs a basic LED TV. Your best response is:",
                "options": [
                    "A) Offer an immediate discount",
                    "B) Agree and show a cheaper model",
                    "C) Explain Mini-LED contrast and Google TV value vs basic LED",
                    "D) Say nothing and wait",
                ],
                "answer": "C",
                "pts": 1,
            },
        ],
    },
    "c7l_silver": {
        "name": "C7L Silver Quiz",
        "product": "TCL C7L",
        "level": "silver",
        "pass_pct": 75,
        "questions": [
            {
                "q": "What does VRR stand for and why does it matter for gamers?",
                "options": [
                    "A) Variable Refresh Rate — eliminates screen tearing",
                    "B) Video Render Resolution — improves picture quality",
                    "C) Virtual Reality Ready — enables VR headsets",
                    "D) Volume Range Reduction — audio feature",
                ],
                "answer": "A",
                "pts": 1,
            },
            {
                "q": "Compared to Samsung QLED at the same price, the C7L Mini-LED offers:",
                "options": [
                    "A) Fewer dimming zones",
                    "B) More local dimming zones and deeper blacks",
                    "C) Same panel performance",
                    "D) Lower peak brightness",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "Which C7L feature is most relevant for a customer who streams Netflix and Disney+?",
                "options": ["A) HDMI 2.1", "B) Google TV with built-in streaming apps", "C) VRR", "D) Dolby Vision only"],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "What is the correct AIDA selling structure?",
                "options": [
                    "A) Ask, Inform, Demonstrate, Agree",
                    "B) Attention, Interest, Desire, Action",
                    "C) Approach, Identify, Display, Advise",
                    "D) Attract, Introduce, Decide, Accept",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "A customer is leaving without buying. What is the best closing technique?",
                "options": [
                    "A) Let them go — never push",
                    "B) Ask what is stopping them and address the specific objection",
                    "C) Immediately offer 20% off",
                    "D) Call the manager",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "The C7L's peak brightness (nits) is approximately:",
                "options": ["A) 300 nits", "B) 500 nits", "C) 1000+ nits", "D) 150 nits"],
                "answer": "C",
                "pts": 1,
            },
            {
                "q": "What HDR format does the C7L support?",
                "options": ["A) HDR10 only", "B) Dolby Vision, HDR10+, HLG", "C) SDR only", "D) HDR10 and HLG only"],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "A customer asks why they should buy TCL over LG. Your strongest point is:",
                "options": [
                    "A) TCL is a Chinese brand so it's cheaper quality",
                    "B) TCL is a global Olympic partner with Mini-LED tech at mid-range pricing",
                    "C) LG is better but TCL is cheaper",
                    "D) Both brands are the same",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "Which port is required for 4K 120Hz gaming on the C7L?",
                "options": ["A) USB-A", "B) HDMI 2.0", "C) HDMI 2.1", "D) DisplayPort"],
                "answer": "C",
                "pts": 1,
            },
            {
                "q": "What is the recommended first step when approaching a customer in-store?",
                "options": [
                    "A) Start listing all specs immediately",
                    "B) Ask about their usage — gaming, movies, or general viewing",
                    "C) Show the most expensive model first",
                    "D) Hand them a brochure and wait",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "TCL's C7L Mini-LED uses how many dimming zones compared to standard LED?",
                "options": [
                    "A) Same number",
                    "B) Far more zones — enables precise local dimming",
                    "C) Fewer zones",
                    "D) Mini-LED has no dimming zones",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "Which available size range best describes the C7L lineup?",
                "options": ["A) 32\" – 43\"", "B) 43\" – 55\"", "C) 55\" – 98\"", "D) 65\" – 115\""],
                "answer": "C",
                "pts": 1,
            },
            {
                "q": "Scenario: A family wants a TV for a bright living room. Which C7L feature do you highlight?",
                "options": [
                    "A) Dolby Atmos audio",
                    "B) High peak brightness and anti-glare screen",
                    "C) HDMI 2.1 for gaming",
                    "D) Number of USB ports",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "What does Google TV offer over a standard smart TV interface?",
                "options": [
                    "A) Nothing extra",
                    "B) Unified content discovery, Google Assistant, and app ecosystem",
                    "C) Only YouTube access",
                    "D) Requires a smartphone to work",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "What is the ideal way to open a demo of the C7L in-store?",
                "options": [
                    "A) Show a static image",
                    "B) Play a dark movie scene to show contrast and blacks",
                    "C) Leave it on a news channel",
                    "D) Turn brightness to minimum",
                ],
                "answer": "B",
                "pts": 1,
            },
        ],
    },
}


# ── Data helpers ─────────────────────────────────────────────────────────────

def load() -> dict:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return {"promoters": {}, "competitions": {}}


def save(data: dict) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2))


def get_level(pts: int) -> str:
    for threshold, name in LEVELS:
        if pts >= threshold:
            return name
    return "Bronze"


def get_promoter(data: dict, pid: str) -> dict | None:
    return data["promoters"].get(pid)


def require_promoter(data: dict, pid: str) -> dict:
    p = get_promoter(data, pid)
    if not p:
        print(f"Promoter '{pid}' not found. Run: python tcl_training.py promoter list")
        sys.exit(1)
    return p


def add_points(promoter: dict, pts: int, reason: str) -> None:
    promoter["points"] = promoter.get("points", 0) + pts
    promoter["level"] = get_level(promoter["points"])
    promoter.setdefault("history", []).append({"date": TODAY, "pts": pts, "reason": reason})


def next_id(data: dict) -> str:
    existing = [int(k[1:]) for k in data["promoters"] if k.startswith("P")]
    return f"P{(max(existing) + 1 if existing else 1):03d}"


# ── Commands: promoter ───────────────────────────────────────────────────────

def cmd_promoter_add(data: dict, args: list) -> None:
    if len(args) < 2:
        print("Usage: promoter add <name> <store>")
        sys.exit(1)
    name, store = args[0], args[1]
    pid = next_id(data)
    data["promoters"][pid] = {
        "id": pid,
        "name": name,
        "store": store,
        "joined": TODAY,
        "points": 0,
        "level": "Bronze",
        "quiz_results": [],
        "comp_entries": [],
        "history": [],
    }
    save(data)
    print(f"Promoter registered: {pid}  |  {name}  |  {store}")


def cmd_promoter_list(data: dict) -> None:
    ps = list(data["promoters"].values())
    if not ps:
        print("No promoters registered yet. Use: promoter add <name> <store>")
        return
    ps.sort(key=lambda x: x["points"], reverse=True)
    print(f"\n  {'ID':<6} {'Name':<22} {'Store':<20} {'Pts':>5}  Level")
    print("  " + "─" * 62)
    for p in ps:
        badge = LEVEL_BADGES[p["level"]]
        print(f"  {p['id']:<6} {p['name']:<22} {p['store']:<20} {p['points']:>5}  {badge} {p['level']}")
    print()


def cmd_promoter_show(data: dict, args: list) -> None:
    if not args:
        print("Usage: promoter show <id>")
        sys.exit(1)
    p = require_promoter(data, args[0].upper())
    badge = LEVEL_BADGES[p["level"]]
    print(f"\n  ── Promoter Profile ───────────────────────────")
    print(f"  ID:      {p['id']}")
    print(f"  Name:    {p['name']}")
    print(f"  Store:   {p['store']}")
    print(f"  Joined:  {p['joined']}")
    print(f"  Points:  {p['points']}  |  Level: {badge} {p['level']}")

    if p["quiz_results"]:
        print(f"\n  Quiz Results:")
        for r in p["quiz_results"]:
            status = "PASS ✓" if r["passed"] else "FAIL ✗"
            print(f"    {r['quiz']:16}  {r['score']:>2}/{r['total']}  ({r['pct']}%)  {status}  {r['date']}")

    if p["comp_entries"]:
        print(f"\n  Competition Entries:")
        for e in p["comp_entries"]:
            print(f"    {e['comp']:20}  Score: {e['weighted_score']:.1f}/4.0  Rank: {e.get('rank','–')}  {e['date']}")

    if p["history"]:
        print(f"\n  Points History:")
        for h in p["history"][-5:]:
            sign = "+" if h["pts"] >= 0 else ""
            print(f"    {h['date']}  {sign}{h['pts']} pts  —  {h['reason']}")
    print()


# ── Commands: quiz ───────────────────────────────────────────────────────────

def cmd_quiz_list() -> None:
    print("\n  Available Quizzes:")
    print(f"  {'ID':<16} {'Name':<28} {'Level':<8} {'Questions':<10} Pass%")
    print("  " + "─" * 68)
    for qid, q in QUIZ_BANK.items():
        n = len(q["questions"])
        print(f"  {qid:<16} {q['name']:<28} {q['level']:<8} {n:<10} {q['pass_pct']}%")
    print()


def cmd_quiz_run(data: dict, args: list) -> None:
    if len(args) < 2:
        print("Usage: quiz run <quiz_id> <promoter_id>")
        sys.exit(1)
    qid, pid = args[0], args[1].upper()
    quiz = QUIZ_BANK.get(qid)
    if not quiz:
        print(f"Quiz '{qid}' not found. Run: quiz list")
        sys.exit(1)
    p = require_promoter(data, pid)

    print(f"\n  ── {quiz['name']} for {p['name']} ─────────────────────")
    print(f"  {len(quiz['questions'])} questions  |  Pass: {quiz['pass_pct']}%  |  Type your answer (A/B/C/D)\n")

    score = 0
    total = sum(q["pts"] for q in quiz["questions"])

    for i, q in enumerate(quiz["questions"], 1):
        print(f"  Q{i}. {q['q']}")
        for opt in q["options"]:
            print(f"      {opt}")
        while True:
            ans = input("  Answer: ").strip().upper()
            if ans in ("A", "B", "C", "D"):
                break
            print("  Please enter A, B, C, or D.")
        if ans == q["answer"]:
            score += q["pts"]
            print("  ✓ Correct!\n")
        else:
            print(f"  ✗ Incorrect. Correct answer: {q['answer']}\n")

    pct = int(score / total * 100)
    passed = pct >= quiz["pass_pct"]
    status = "PASSED ✓" if passed else "FAILED ✗"
    print(f"  ── Result: {score}/{total}  ({pct}%)  {status} ──────────────────")

    pts_earned = 0
    if passed:
        level_key = f"quiz_{quiz['level']}"
        pts_earned += POINTS_MAP.get(level_key, 10)
        add_points(p, pts_earned, f"{quiz['name']} pass")
        if pct == 100:
            bonus = POINTS_MAP["quiz_perfect_bonus"]
            pts_earned += bonus
            add_points(p, bonus, f"{quiz['name']} perfect score bonus")
        print(f"  Points earned: +{pts_earned}  |  New total: {p['points']}  ({p['level']})")
    else:
        print(f"  No points awarded. Retake to pass (need {quiz['pass_pct']}%).")

    p["quiz_results"].append({
        "quiz": qid,
        "score": score,
        "total": total,
        "pct": pct,
        "passed": passed,
        "date": TODAY,
    })
    save(data)


# ── Commands: leaderboard ────────────────────────────────────────────────────

def cmd_leaderboard(data: dict) -> None:
    ps = sorted(data["promoters"].values(), key=lambda x: x["points"], reverse=True)
    if not ps:
        print("No promoters yet.")
        return

    print(f"\n  TCL PROMOTER LEADERBOARD — {date.today().strftime('%B %Y').upper()}")
    print(f"  {'Rank':<5} {'Name':<22} {'Store':<20} {'Pts':>5}  Level")
    print("  " + "═" * 62)
    for i, p in enumerate(ps, 1):
        badge = LEVEL_BADGES[p["level"]]
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"  {i}.")
        print(f"  {medal:<5} {p['name']:<22} {p['store']:<20} {p['points']:>5}  {badge} {p['level']}")
    print()
    if ps:
        print(f"  Leader: {ps[0]['name']} with {ps[0]['points']} pts")
        done = sum(1 for p in ps if p["level"] != "Bronze")
        print(f"  Above Bronze: {done}/{len(ps)} promoters\n")


# ── Commands: competition ────────────────────────────────────────────────────

def cmd_comp_new(data: dict, args: list) -> None:
    if not args:
        print("Usage: comp new <name>")
        sys.exit(1)
    name = " ".join(args)
    existing = [int(k[1:]) for k in data["competitions"] if k.startswith("C")]
    cid = f"C{(max(existing) + 1 if existing else 1):03d}"
    data["competitions"][cid] = {
        "id": cid,
        "name": name,
        "date": TODAY,
        "entries": [],
        "ranked": False,
    }
    save(data)
    print(f"Competition created: {cid}  |  {name}")


def cmd_comp_list(data: dict) -> None:
    comps = list(data["competitions"].values())
    if not comps:
        print("No competitions yet. Use: comp new <name>")
        return
    print(f"\n  {'ID':<8} {'Name':<35} {'Date':<12} Entries")
    print("  " + "─" * 60)
    for c in comps:
        print(f"  {c['id']:<8} {c['name']:<35} {c['date']:<12} {len(c['entries'])}")
    print()


def cmd_comp_score(data: dict, args: list) -> None:
    if len(args) < 2:
        print("Usage: comp score <comp_id> <promoter_id>")
        sys.exit(1)
    cid, pid = args[0].upper(), args[1].upper()
    comp = data["competitions"].get(cid)
    if not comp:
        print(f"Competition '{cid}' not found. Run: comp list")
        sys.exit(1)
    p = require_promoter(data, pid)

    already = any(e["promoter_id"] == pid for e in comp["entries"])
    if already:
        print(f"{p['name']} already has an entry in {comp['name']}. Use comp results to see scores.")
        sys.exit(1)

    print(f"\n  Scoring: {p['name']}  in  {comp['name']}")
    print("  Rate each criterion 1–4  (1=Poor  2=OK  3=Good  4=Excellent)\n")

    scores = {}
    criteria_labels = {"knowledge": "Product Knowledge (35%)", "creativity": "Creativity (25%)", "selling": "Selling Skills (40%)"}
    for key, label in criteria_labels.items():
        while True:
            raw = input(f"  {label}: ").strip()
            if raw in ("1", "2", "3", "4"):
                scores[key] = int(raw)
                break
            print("  Please enter 1, 2, 3, or 4.")

    weighted = sum(scores[k] * RUBRIC[k] for k in scores)
    pct = int(weighted / 4 * 100)

    print(f"\n  ── Score: {weighted:.2f}/4.00  ({pct}%) ────────────────────────")
    for k, v in scores.items():
        print(f"     {criteria_labels[k]:<35}  {v}/4")

    entry = {
        "promoter_id": pid,
        "promoter_name": p["name"],
        "store": p["store"],
        "scores": scores,
        "weighted_score": round(weighted, 3),
        "pct": pct,
        "date": TODAY,
    }
    comp["entries"].append(entry)

    # Award comp submission points
    add_points(p, POINTS_MAP["comp_submit"], f"Submitted to {comp['name']}")
    p["comp_entries"].append({
        "comp": cid,
        "weighted_score": round(weighted, 3),
        "date": TODAY,
    })
    save(data)
    print(f"\n  Entry saved. Submission points (+{POINTS_MAP['comp_submit']}) awarded to {p['name']}.")
    print(f"  Run 'comp rank {cid}' after all entries to finalize rankings.\n")


def cmd_comp_rank(data: dict, args: list) -> None:
    if not args:
        print("Usage: comp rank <comp_id>")
        sys.exit(1)
    cid = args[0].upper()
    comp = data["competitions"].get(cid)
    if not comp:
        print(f"Competition '{cid}' not found.")
        sys.exit(1)
    if not comp["entries"]:
        print("No entries yet.")
        return

    ranked = sorted(comp["entries"], key=lambda e: e["weighted_score"], reverse=True)

    print(f"\n  ── {comp['name']} — FINAL RANKINGS ───────────────────")
    print(f"  {'Rank':<6} {'Promoter':<22} {'Store':<18} {'Score':>7}  {'%':>5}")
    print("  " + "─" * 60)

    award_pts = {1: POINTS_MAP["comp_1st"], 2: POINTS_MAP["comp_2nd"], 3: POINTS_MAP["comp_3rd"]}
    award_sar = {1: "1,000 SAR 🥇", 2: "800 SAR 🥈", 3: "600 SAR 🥉"}

    for i, entry in enumerate(ranked, 1):
        medal = {1: "🥇 1st", 2: "🥈 2nd", 3: "🥉 3rd"}.get(i, f"   {i}th")
        print(f"  {medal:<6} {entry['promoter_name']:<22} {entry['store']:<18} {entry['weighted_score']:>7.3f}  {entry['pct']:>4}%")

        # Assign rank on entry and award points (only first time)
        e_ref = next(e for e in comp["entries"] if e["promoter_id"] == entry["promoter_id"])
        if "rank" not in e_ref:
            e_ref["rank"] = i
            if i <= 3:
                p = get_promoter(data, entry["promoter_id"])
                if p:
                    pts = award_pts[i]
                    add_points(p, pts, f"{comp['name']} rank #{i}")
                    p_entry = next((x for x in p["comp_entries"] if x["comp"] == cid), None)
                    if p_entry:
                        p_entry["rank"] = i

    comp["ranked"] = True
    save(data)

    print(f"\n  {'Promoter':<22} Award")
    print("  " + "─" * 40)
    for i, entry in enumerate(ranked[:3], 1):
        print(f"  {entry['promoter_name']:<22} {award_sar[i]}")
    print()
    print("  Rankings saved. Award points distributed to top 3.\n")


def cmd_comp_results(data: dict, args: list) -> None:
    if not args:
        print("Usage: comp results <comp_id>")
        sys.exit(1)
    cid = args[0].upper()
    comp = data["competitions"].get(cid)
    if not comp:
        print(f"Competition '{cid}' not found.")
        sys.exit(1)
    if not comp["entries"]:
        print("No entries yet.")
        return

    ranked = sorted(comp["entries"], key=lambda e: e["weighted_score"], reverse=True)
    print(f"\n  {comp['name']}  |  {comp['date']}  |  {len(ranked)} entries")
    print(f"  Rubric: Knowledge 35%  ·  Creativity 25%  ·  Selling 40%\n")
    print(f"  {'#':<4} {'Promoter':<22} {'Knwl':>5} {'Crtv':>5} {'Sell':>5} {'Score':>7}  {'%':>5}")
    print("  " + "─" * 58)
    for i, e in enumerate(ranked, 1):
        s = e["scores"]
        print(f"  {i:<4} {e['promoter_name']:<22} {s['knowledge']:>5} {s['creativity']:>5} {s['selling']:>5} {e['weighted_score']:>7.3f}  {e['pct']:>4}%")
    print()


# ── Main ─────────────────────────────────────────────────────────────────────

USAGE = """
  TCL Electronics KSA — Promoter Training System

  PROMOTER MANAGEMENT
    promoter add  <name> <store>     Register a new promoter
    promoter list                    List all promoters
    promoter show <id>               Show promoter profile and history

  QUIZZES
    quiz list                        List available quizzes
    quiz run  <quiz_id> <promoter_id>  Run an interactive quiz

  LEADERBOARD
    leaderboard                      Show ranked standings

  COMPETITIONS
    comp new     <name>              Create a new competition
    comp list                        List all competitions
    comp score   <comp_id> <promo_id>  Score a promoter's entry
    comp rank    <comp_id>           Finalize rankings + award points
    comp results <comp_id>           View competition results table

  EXAMPLES
    python tcl_training.py promoter add "Ahmed Ali" "Riyadh Mall"
    python tcl_training.py quiz run c7l_bronze P001
    python tcl_training.py leaderboard
    python tcl_training.py comp new "C7L Phase 2 Live Demo"
    python tcl_training.py comp score C001 P001
    python tcl_training.py comp rank C001
"""


def main() -> None:
    data = load()
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        print(USAGE)
        return

    cmd = args[0]
    sub = args[1] if len(args) > 1 else ""
    rest = args[2:]

    dispatch = {
        ("promoter", "add"):     lambda: cmd_promoter_add(data, rest),
        ("promoter", "list"):    lambda: cmd_promoter_list(data),
        ("promoter", "show"):    lambda: cmd_promoter_show(data, rest),
        ("quiz",     "list"):    lambda: cmd_quiz_list(),
        ("quiz",     "run"):     lambda: cmd_quiz_run(data, rest),
        ("leaderboard", ""):     lambda: cmd_leaderboard(data),
        ("comp",     "new"):     lambda: cmd_comp_new(data, rest),
        ("comp",     "list"):    lambda: cmd_comp_list(data),
        ("comp",     "score"):   lambda: cmd_comp_score(data, rest),
        ("comp",     "rank"):    lambda: cmd_comp_rank(data, rest),
        ("comp",     "results"): lambda: cmd_comp_results(data, rest),
    }

    fn = dispatch.get((cmd, sub))
    if fn:
        fn()
    else:
        print(f"Unknown command: {cmd} {sub}")
        print(USAGE)
        sys.exit(1)


if __name__ == "__main__":
    main()
