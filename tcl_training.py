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
    "c7l_gold": {
        "name": "C7L Gold Quiz",
        "product": "TCL C7L",
        "level": "gold",
        "pass_pct": 85,
        "questions": [
            {
                "q": "A customer with a 65\" C7L reports motion blur during fast sports. What do you advise?",
                "options": [
                    "A) Tell them it's a defect and offer a refund",
                    "B) Enable Motion Clarity / MEMC in the picture settings",
                    "C) Suggest they buy a different brand",
                    "D) Reduce the refresh rate",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "Which local dimming setting gives the best contrast on the C7L for a dark room?",
                "options": ["A) Off", "B) Low", "C) Medium", "D) High"],
                "answer": "D",
                "pts": 1,
            },
            {
                "q": "A customer asks about the difference between Dolby Vision and HDR10+. You say:",
                "options": [
                    "A) They are identical formats",
                    "B) Dolby Vision uses dynamic metadata per-scene; HDR10+ does too but via a different ecosystem",
                    "C) HDR10+ is always better",
                    "D) Neither format matters for picture quality",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "A competitor's promoter tells a customer that OLED has better picture than Mini-LED. How do you respond?",
                "options": [
                    "A) Agree — OLED is always better",
                    "B) Explain that Mini-LED offers higher peak brightness and no burn-in risk at a better price point",
                    "C) Say nothing",
                    "D) Offer a bigger discount immediately",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "What is the benefit of the C7L's ALLM (Auto Low Latency Mode)?",
                "options": [
                    "A) Automatically adjusts volume",
                    "B) Switches to Game mode automatically when a console is detected, reducing input lag",
                    "C) Enables automatic software updates",
                    "D) Increases brightness when gaming",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "A customer wants the best picture for HDR movies at home in a dim room. Which picture mode?",
                "options": ["A) Vivid", "B) Standard", "C) Movie / Cinema", "D) Dynamic"],
                "answer": "C",
                "pts": 1,
            },
            {
                "q": "The C7L supports eARC on which HDMI port?",
                "options": ["A) HDMI 1", "B) HDMI 2", "C) HDMI 3 (eARC)", "D) All ports support eARC"],
                "answer": "C",
                "pts": 1,
            },
            {
                "q": "A customer already owns a Sonos soundbar. Which C7L feature ensures best audio compatibility?",
                "options": ["A) Bluetooth only", "B) eARC for lossless audio passthrough", "C) Built-in speakers", "D) Optical out only"],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "What is the correct way to describe TCL's Olympic partnership to a customer?",
                "options": [
                    "A) TCL sponsors local sports only",
                    "B) TCL is a Worldwide Olympic Partner — same tier as Coca-Cola and Samsung",
                    "C) TCL sponsors the Olympics in China only",
                    "D) TCL is an unofficial Olympic supporter",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "A customer asks if the C7L will support new apps in 3 years. Your answer:",
                "options": [
                    "A) No guarantees",
                    "B) Google TV receives ongoing updates and new apps via the Play Store",
                    "C) The TV will need replacement in 2 years",
                    "D) Only pre-installed apps are available",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "Which C7L feature is most relevant for a customer with a PS5 or Xbox Series X?",
                "options": [
                    "A) Built-in Chromecast",
                    "B) HDMI 2.1 with 4K 120Hz + VRR + ALLM",
                    "C) USB recording",
                    "D) Dolby Atmos audio",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "A customer is deciding between 55\" and 65\" C7L for a 3-metre viewing distance. You recommend:",
                "options": [
                    "A) 55\" — bigger is always worse",
                    "B) 65\" — at 3m the larger screen gives a more immersive 4K experience",
                    "C) Neither — they need a projector",
                    "D) 55\" only if they watch sports",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "What does the 'Mini' in Mini-LED refer to?",
                "options": [
                    "A) A smaller TV size",
                    "B) Thousands of tiny LED backlights enabling precise zone dimming",
                    "C) A mini remote control",
                    "D) Reduced power consumption only",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "After closing a C7L sale, what is the ideal next step to build loyalty?",
                "options": [
                    "A) Walk away immediately",
                    "B) Help set up Google TV, show key features, and share TCL support contact",
                    "C) Upsell a different brand's accessories",
                    "D) Hand them a warranty card and say goodbye",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "A store manager asks you to summarise why C7L outsells competitors in your region. You say:",
                "options": [
                    "A) Price is the only reason",
                    "B) Best Mini-LED contrast at mid-range price + Google TV ecosystem + Olympic brand credibility",
                    "C) Marketing budget is higher",
                    "D) The warranty is longer",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "A customer saw the C7L cheaper online. What is the best response?",
                "options": [
                    "A) Match the price immediately",
                    "B) Highlight in-store value: setup support, warranty service, and hands-on demo experience",
                    "C) Tell them to buy online",
                    "D) Ignore the objection",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "What picture setting should you AVOID leaving on during a demo to prevent screen burn perception?",
                "options": ["A) Movie mode", "B) Static logo channel for extended periods", "C) HDR content", "D) Low brightness"],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "The C7L's Dolby Atmos support means:",
                "options": [
                    "A) The TV has built-in ceiling speakers",
                    "B) It can decode and pass through Dolby Atmos object-based audio to compatible soundbars",
                    "C) Audio quality is the same as any TV",
                    "D) Only stereo sound is supported",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "Which selling technique is most effective after a customer says 'I need to think about it'?",
                "options": [
                    "A) End the conversation",
                    "B) Ask 'What specifically would you like to think about?' to uncover the real objection",
                    "C) Offer a 50% discount",
                    "D) Call them the next day",
                ],
                "answer": "B",
                "pts": 1,
            },
            {
                "q": "To qualify for Gold level in the TCL promoter programme, a promoter needs how many points?",
                "options": ["A) 50", "B) 75", "C) 100", "D) 150"],
                "answer": "C",
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


# ── Commands: report ─────────────────────────────────────────────────────────

def cmd_report(data: dict) -> None:
    ps = sorted(data["promoters"].values(), key=lambda x: x["points"], reverse=True)
    comps = list(data["competitions"].values())
    month = date.today().strftime("%B %Y")

    sep = "═" * 66

    print(f"\n  {sep}")
    print(f"  TCL ELECTRONICS KSA — PROMOTER TRAINING REPORT")
    print(f"  Generated: {TODAY}  |  Period: {month}")
    print(f"  {sep}\n")

    # ── Summary stats ──
    total_p = len(ps)
    if total_p == 0:
        print("  No promoters registered yet.")
        return

    avg_pts = sum(p["points"] for p in ps) / total_p
    levels_count = {}
    for p in ps:
        levels_count[p["level"]] = levels_count.get(p["level"], 0) + 1

    print(f"  SUMMARY")
    print(f"  {'─' * 40}")
    print(f"  Total promoters     : {total_p}")
    print(f"  Average points      : {avg_pts:.1f}")
    print(f"  Competitions run    : {len(comps)}")
    print()
    for lvl, badge in LEVEL_BADGES.items():
        count = levels_count.get(lvl, 0)
        bar = "█" * count
        print(f"  {badge} {lvl:<10} : {count:>3}  {bar}")
    print()

    # ── Leaderboard ──
    print(f"  LEADERBOARD")
    print(f"  {'─' * 40}")
    print(f"  {'#':<4} {'Name':<22} {'Store':<20} {'Pts':>5}  Level")
    for i, p in enumerate(ps, 1):
        badge = LEVEL_BADGES[p["level"]]
        medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(i, f"  {i}.")
        print(f"  {medal:<4} {p['name']:<22} {p['store']:<20} {p['points']:>5}  {badge} {p['level']}")
    print()

    # ── Quiz performance ──
    print(f"  QUIZ PERFORMANCE")
    print(f"  {'─' * 40}")
    print(f"  {'Name':<22} {'Quizzes':>8} {'Passed':>7} {'Avg %':>7}  Highest")
    for p in ps:
        results = p.get("quiz_results", [])
        if not results:
            print(f"  {p['name']:<22} {'—':>8}")
            continue
        passed = [r for r in results if r["passed"]]
        avg = int(sum(r["pct"] for r in results) / len(results))
        best = max(results, key=lambda r: r["pct"])
        print(f"  {p['name']:<22} {len(results):>8} {len(passed):>7} {avg:>6}%  {best['quiz']} ({best['pct']}%)")
    print()

    # ── Competition history ──
    if comps:
        print(f"  COMPETITION RESULTS")
        print(f"  {'─' * 40}")
        for c in comps:
            if not c["entries"]:
                continue
            ranked = sorted(c["entries"], key=lambda e: e["weighted_score"], reverse=True)
            print(f"  {c['name']}  ({c['date']})")
            for i, e in enumerate(ranked[:3], 1):
                medal = {1: "🥇", 2: "🥈", 3: "🥉"}[i]
                print(f"    {medal} {e['promoter_name']:<22} {e['weighted_score']:.3f}/4.00  ({e['pct']}%)")
            print()

    # ── Next steps ──
    print(f"  RECOMMENDED NEXT STEPS")
    print(f"  {'─' * 40}")
    no_quiz = [p["name"] for p in ps if not p.get("quiz_results")]
    if no_quiz:
        print(f"  • Pending first quiz : {', '.join(no_quiz)}")
    bronze_only = [p["name"] for p in ps if p["level"] == "Bronze" and p["points"] > 0]
    if bronze_only:
        print(f"  • Push to Silver (50 pts): {', '.join(bronze_only)}")
    top = ps[0] if ps else None
    if top:
        next_lvl = next((name for thr, name in reversed(LEVELS) if thr > top["points"]), None)
        if next_lvl:
            gap = next(thr for thr, name in LEVELS if name == next_lvl) - top["points"]
            print(f"  • Leader {top['name']} needs {gap} more pts to reach {next_lvl}")
    print(f"\n  {sep}\n")


# ── New Tool 1: promoter edit ────────────────────────────────────────────────

def cmd_promoter_edit(data: dict, args: list) -> None:
    if len(args) < 3:
        print("Usage: promoter edit <id> <name|store> <new_value>")
        sys.exit(1)
    pid, field = args[0].upper(), args[1].lower()
    value = " ".join(args[2:])
    if field not in ("name", "store"):
        print("Field must be 'name' or 'store'.")
        sys.exit(1)
    p = require_promoter(data, pid)
    old = p[field]
    p[field] = value
    save(data)
    print(f"Updated {pid} {field}: '{old}' → '{value}'")


# ── New Tool 2: promoter delete ──────────────────────────────────────────────

def cmd_promoter_delete(data: dict, args: list) -> None:
    if not args:
        print("Usage: promoter delete <id>")
        sys.exit(1)
    pid = args[0].upper()
    p = require_promoter(data, pid)
    confirm = input(f"Delete {p['name']} ({pid})? Type YES to confirm: ").strip()
    if confirm != "YES":
        print("Cancelled.")
        return
    del data["promoters"][pid]
    save(data)
    print(f"Promoter {pid} ({p['name']}) deleted.")


# ── New Tool 3: promoter search ──────────────────────────────────────────────

def cmd_promoter_search(data: dict, args: list) -> None:
    if not args:
        print("Usage: promoter search <keyword>")
        sys.exit(1)
    kw = " ".join(args).lower()
    results = [p for p in data["promoters"].values()
               if kw in p["name"].lower() or kw in p["store"].lower()]
    if not results:
        print(f"No promoters found matching '{kw}'.")
        return
    print(f"\n  Results for '{kw}':")
    for p in results:
        badge = LEVEL_BADGES[p["level"]]
        print(f"  {p['id']}  {p['name']:<22}  {p['store']:<20}  {p['points']} pts  {badge} {p['level']}")
    print()


# ── New Tool 4: promoter stats ───────────────────────────────────────────────

def cmd_promoter_stats(data: dict, args: list) -> None:
    if not args:
        print("Usage: promoter stats <id>")
        sys.exit(1)
    p = require_promoter(data, args[0].upper())
    badge = LEVEL_BADGES[p["level"]]
    results = p.get("quiz_results", [])
    passed = [r for r in results if r["passed"]]
    comps = p.get("comp_entries", [])

    print(f"\n  ── Stats: {p['name']} ({p['id']}) ─────────────────────────")
    print(f"  Level  : {badge} {p['level']}  |  Points: {p['points']}")
    print(f"  Store  : {p['store']}  |  Joined: {p['joined']}")
    print(f"\n  Quiz Performance:")
    if results:
        avg_pct = int(sum(r["pct"] for r in results) / len(results))
        best = max(results, key=lambda r: r["pct"])
        print(f"    Taken: {len(results)}  |  Passed: {len(passed)}  |  Avg: {avg_pct}%  |  Best: {best['quiz']} ({best['pct']}%)")
    else:
        print(f"    No quizzes taken yet.")
    print(f"\n  Competitions:")
    if comps:
        avg_score = sum(e["weighted_score"] for e in comps) / len(comps)
        print(f"    Entered: {len(comps)}  |  Avg score: {avg_score:.2f}/4.00")
    else:
        print(f"    No competitions entered.")
    next_level = next((name for thr, name in reversed(LEVELS) if thr > p["points"]), None)
    if next_level:
        gap = next(thr for thr, name in LEVELS if name == next_level) - p["points"]
        print(f"\n  Next milestone: {gap} pts to reach {next_level}")
    else:
        print(f"\n  Max level reached: Champion!")
    print()


# ── New Tool 5: promoter export ──────────────────────────────────────────────

def cmd_promoter_export(data: dict) -> None:
    import csv, io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Name", "Store", "Joined", "Points", "Level",
                     "Quizzes Taken", "Quizzes Passed", "Comps Entered"])
    for p in data["promoters"].values():
        results = p.get("quiz_results", [])
        passed = sum(1 for r in results if r["passed"])
        writer.writerow([p["id"], p["name"], p["store"], p["joined"],
                         p["points"], p["level"], len(results), passed,
                         len(p.get("comp_entries", []))])
    csv_path = Path(__file__).parent / "promoters_export.csv"
    csv_path.write_text(output.getvalue())
    print(f"Exported {len(data['promoters'])} promoter(s) to {csv_path.name}")


# ── New Tool 6: promoter top ─────────────────────────────────────────────────

def cmd_promoter_top(data: dict, args: list) -> None:
    n = int(args[0]) if args and args[0].isdigit() else 5
    ps = sorted(data["promoters"].values(), key=lambda x: x["points"], reverse=True)[:n]
    if not ps:
        print("No promoters registered yet.")
        return
    print(f"\n  Top {n} Promoters:")
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    for i, p in enumerate(ps, 1):
        badge = LEVEL_BADGES[p["level"]]
        medal = medals.get(i, f"  {i}.")
        print(f"  {medal} {p['name']:<22}  {p['points']:>5} pts  {badge} {p['level']}  —  {p['store']}")
    print()


# ── New Tool 7: quiz stats ───────────────────────────────────────────────────

def cmd_quiz_stats(data: dict) -> None:
    ps = list(data["promoters"].values())
    print(f"\n  ── Quiz Analytics ──────────────────────────────────────")
    for qid, quiz in QUIZ_BANK.items():
        attempts = [r for p in ps for r in p.get("quiz_results", []) if r["quiz"] == qid]
        if not attempts:
            print(f"  {quiz['name']}: no attempts yet")
            continue
        passed = [a for a in attempts if a["passed"]]
        avg_pct = int(sum(a["pct"] for a in attempts) / len(attempts))
        pass_rate = int(len(passed) / len(attempts) * 100)
        print(f"  {quiz['name']}")
        print(f"    Attempts: {len(attempts)}  |  Pass rate: {pass_rate}%  |  Avg score: {avg_pct}%")
    print()


# ── New Tool 8: quiz reset ───────────────────────────────────────────────────

def cmd_quiz_reset(data: dict, args: list) -> None:
    if len(args) < 2:
        print("Usage: quiz reset <quiz_id|all> <promoter_id>")
        sys.exit(1)
    qid, pid = args[0], args[1].upper()
    p = require_promoter(data, pid)
    if qid == "all":
        p["quiz_results"] = []
        save(data)
        print(f"All quiz results cleared for {p['name']}.")
    else:
        before = len(p["quiz_results"])
        p["quiz_results"] = [r for r in p["quiz_results"] if r["quiz"] != qid]
        save(data)
        print(f"Removed {before - len(p['quiz_results'])} result(s) for quiz '{qid}' from {p['name']}.")


# ── New Tool 9: quiz export ──────────────────────────────────────────────────

def cmd_quiz_export(data: dict) -> None:
    import csv, io
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Promoter ID", "Promoter Name", "Store",
                     "Quiz", "Score", "Total", "Pct", "Passed", "Date"])
    for p in data["promoters"].values():
        for r in p.get("quiz_results", []):
            writer.writerow([p["id"], p["name"], p["store"],
                             r["quiz"], r["score"], r["total"], r["pct"], r["passed"], r["date"]])
    csv_path = Path(__file__).parent / "quiz_results_export.csv"
    csv_path.write_text(output.getvalue())
    total = sum(len(p.get("quiz_results", [])) for p in data["promoters"].values())
    print(f"Exported {total} quiz result(s) to {csv_path.name}")


# ── New Tool 10: quiz hard ───────────────────────────────────────────────────

def cmd_quiz_hard(args: list) -> None:
    qid = args[0] if args else "c7l_gold"
    quiz = QUIZ_BANK.get(qid)
    if not quiz:
        print(f"Quiz '{qid}' not found. Run: quiz list")
        sys.exit(1)
    hard_qs = quiz["questions"][-5:]
    print(f"\n  ── Hard Practice: {quiz['name']} (last 5 questions) ───────────")
    score = 0
    for i, q in enumerate(hard_qs, 1):
        print(f"\n  Q{i}. {q['q']}")
        for opt in q["options"]:
            print(f"      {opt}")
        while True:
            ans = input("  Answer: ").strip().upper()
            if ans in ("A", "B", "C", "D"):
                break
            print("  Please enter A, B, C, or D.")
        if ans == q["answer"]:
            score += 1
            print("  ✓ Correct!")
        else:
            print(f"  ✗ Incorrect. Correct answer: {q['answer']}")
    print(f"\n  Practice score: {score}/5  ({score * 20}%)\n")


# ── New Tool 11: quiz review ─────────────────────────────────────────────────

def cmd_quiz_review(args: list) -> None:
    if not args:
        print("Usage: quiz review <quiz_id>")
        sys.exit(1)
    quiz = QUIZ_BANK.get(args[0])
    if not quiz:
        print(f"Quiz '{args[0]}' not found.")
        sys.exit(1)
    print(f"\n  ── {quiz['name']} — Answer Key ─────────────────────────────")
    for i, q in enumerate(quiz["questions"], 1):
        correct_opt = next(o for o in q["options"] if o.startswith(q["answer"] + ")"))
        print(f"  Q{i:>2}. {q['q']}")
        print(f"        Answer: {correct_opt}")
    print()


# ── New Tool 12: quiz bank ───────────────────────────────────────────────────

def cmd_quiz_bank() -> None:
    print(f"\n  ── Full Quiz Bank ──────────────────────────────────────")
    for qid, q in QUIZ_BANK.items():
        print(f"\n  {qid}  |  {q['name']}  |  Level: {q['level'].title()}  |  Pass: {q['pass_pct']}%")
        for i, question in enumerate(q["questions"], 1):
            preview = question["q"][:72] + ("…" if len(question["q"]) > 72 else "")
            print(f"    {i:>2}. {preview}")
    print()


# ── New Tool 13: points add ──────────────────────────────────────────────────

def cmd_points_add(data: dict, args: list) -> None:
    if len(args) < 3:
        print("Usage: points add <promoter_id> <pts> <reason>")
        sys.exit(1)
    pid = args[0].upper()
    try:
        pts = int(args[1])
    except ValueError:
        print("Points must be an integer.")
        sys.exit(1)
    reason = " ".join(args[2:])
    p = require_promoter(data, pid)
    add_points(p, pts, reason)
    save(data)
    print(f"Awarded +{pts} pts to {p['name']} for '{reason}'. Total: {p['points']} ({p['level']})")


# ── New Tool 14: points deduct ───────────────────────────────────────────────

def cmd_points_deduct(data: dict, args: list) -> None:
    if len(args) < 3:
        print("Usage: points deduct <promoter_id> <pts> <reason>")
        sys.exit(1)
    pid = args[0].upper()
    try:
        pts = int(args[1])
    except ValueError:
        print("Points must be an integer.")
        sys.exit(1)
    reason = " ".join(args[2:])
    p = require_promoter(data, pid)
    add_points(p, -pts, f"Deduction: {reason}")
    p["points"] = max(p["points"], 0)
    p["level"] = get_level(p["points"])
    save(data)
    print(f"Deducted -{pts} pts from {p['name']} for '{reason}'. Total: {p['points']} ({p['level']})")


# ── New Tool 15: points history ──────────────────────────────────────────────

def cmd_points_history(data: dict, args: list) -> None:
    if not args:
        print("Usage: points history <promoter_id>")
        sys.exit(1)
    p = require_promoter(data, args[0].upper())
    hist = p.get("history", [])
    if not hist:
        print(f"No points history for {p['name']}.")
        return
    print(f"\n  Points History: {p['name']}  |  Current: {p['points']} pts ({p['level']})")
    print(f"  {'Date':<12} {'Pts':>6}  Reason")
    print("  " + "─" * 55)
    for h in hist:
        sign = "+" if h["pts"] >= 0 else ""
        print(f"  {h['date']:<12} {sign}{h['pts']:>5}  {h['reason']}")
    print()


# ── New Tool 16: coaching log ────────────────────────────────────────────────

def cmd_coaching_log(data: dict, args: list) -> None:
    if len(args) < 2:
        print("Usage: coaching log <promoter_id> <notes>")
        sys.exit(1)
    pid = args[0].upper()
    notes = " ".join(args[1:])
    p = require_promoter(data, pid)
    pts = POINTS_MAP["coaching"]
    add_points(p, pts, f"Coaching: {notes[:40]}")
    p.setdefault("coaching_sessions", []).append({"date": TODAY, "notes": notes})
    save(data)
    print(f"Coaching session logged for {p['name']}. +{pts} pts awarded. Total: {p['points']} ({p['level']})")


# ── New Tool 17: comp delete ─────────────────────────────────────────────────

def cmd_comp_delete(data: dict, args: list) -> None:
    if not args:
        print("Usage: comp delete <comp_id>")
        sys.exit(1)
    cid = args[0].upper()
    comp = data["competitions"].get(cid)
    if not comp:
        print(f"Competition '{cid}' not found.")
        sys.exit(1)
    confirm = input(f"Delete '{comp['name']}' ({cid})? Type YES: ").strip()
    if confirm != "YES":
        print("Cancelled.")
        return
    del data["competitions"][cid]
    save(data)
    print(f"Competition {cid} deleted.")


# ── New Tool 18: comp export ─────────────────────────────────────────────────

def cmd_comp_export(data: dict, args: list) -> None:
    import csv, io
    cid = args[0].upper() if args else None
    comps = ({cid: data["competitions"][cid]} if cid and cid in data["competitions"]
             else data["competitions"])
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Competition", "Date", "Promoter ID", "Promoter Name", "Store",
                     "Knowledge", "Creativity", "Selling", "Weighted Score", "Pct", "Rank"])
    total = 0
    for comp in comps.values():
        for e in sorted(comp["entries"], key=lambda x: x["weighted_score"], reverse=True):
            writer.writerow([comp["name"], comp["date"], e["promoter_id"], e["promoter_name"],
                             e["store"], e["scores"]["knowledge"], e["scores"]["creativity"],
                             e["scores"]["selling"], e["weighted_score"], e["pct"], e.get("rank", "–")])
            total += 1
    csv_path = Path(__file__).parent / "competitions_export.csv"
    csv_path.write_text(output.getvalue())
    print(f"Exported {total} entry/entries to {csv_path.name}")


# ── New Tool 19: comp stats ──────────────────────────────────────────────────

def cmd_comp_stats(data: dict) -> None:
    comps = list(data["competitions"].values())
    if not comps:
        print("No competitions yet.")
        return
    all_entries = [e for c in comps for e in c["entries"]]
    print(f"\n  ── Competition Analytics ────────────────────────────────")
    print(f"  Total competitions : {len(comps)}")
    print(f"  Total entries      : {len(all_entries)}")
    if all_entries:
        avg = sum(e["weighted_score"] for e in all_entries) / len(all_entries)
        best = max(all_entries, key=lambda e: e["weighted_score"])
        print(f"  Avg weighted score : {avg:.2f}/4.00")
        print(f"  All-time best      : {best['weighted_score']:.2f} by {best['promoter_name']}")
    print()
    for c in comps:
        if not c["entries"]:
            continue
        avg = sum(e["weighted_score"] for e in c["entries"]) / len(c["entries"])
        print(f"  {c['name']:<40} entries: {len(c['entries'])}  avg: {avg:.2f}/4.00")
    print()


# ── New Tool 20: comp top ────────────────────────────────────────────────────

def cmd_comp_top(data: dict) -> None:
    winners = [(c, next((e for e in c["entries"] if e.get("rank") == 1), None))
               for c in data["competitions"].values()]
    winners = [(c, w) for c, w in winners if w]
    if not winners:
        print("No competition winners yet. Run 'comp rank <id>' to finalize rankings.")
        return
    print(f"\n  ── All-Time Competition Champions ───────────────────────")
    for c, w in winners:
        print(f"  🥇 {c['name']:<38} {w['promoter_name']}  ({w['weighted_score']:.2f}/4.00)")
    print()


# ── New Tool 21: backup ──────────────────────────────────────────────────────

def cmd_backup(data: dict) -> None:
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = Path(__file__).parent / f"backup_{ts}.json"
    backup_path.write_text(json.dumps(data, indent=2))
    print(f"Data backed up to {backup_path.name}")


# ── New Tool 22: restore ─────────────────────────────────────────────────────

def cmd_restore(args: list) -> None:
    if not args:
        backups = sorted(Path(__file__).parent.glob("backup_*.json"))
        if not backups:
            print("No backups found. Usage: restore <backup_filename>")
            return
        print("Available backups:")
        for b in backups:
            print(f"  {b.name}")
        print("Usage: restore <backup_filename>")
        return
    backup_path = Path(__file__).parent / args[0]
    if not backup_path.exists():
        print(f"Backup file '{args[0]}' not found.")
        sys.exit(1)
    confirm = input(f"Restore from {args[0]}? Current data will be overwritten. Type YES: ").strip()
    if confirm != "YES":
        print("Cancelled.")
        return
    restored = json.loads(backup_path.read_text())
    DATA_FILE.write_text(json.dumps(restored, indent=2))
    print(f"Data restored from {args[0]}.")


# ── New Tool 23: import ──────────────────────────────────────────────────────

def cmd_import_csv(data: dict, args: list) -> None:
    import csv
    if not args:
        print("Usage: import <csv_file>")
        print("CSV must have columns: Name, Store")
        sys.exit(1)
    csv_path = Path(__file__).parent / args[0]
    if not csv_path.exists():
        print(f"File '{args[0]}' not found.")
        sys.exit(1)
    added = 0
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = row.get("Name", "").strip()
            store = row.get("Store", "").strip()
            if not name or not store:
                continue
            pid = next_id(data)
            data["promoters"][pid] = {
                "id": pid, "name": name, "store": store, "joined": TODAY,
                "points": 0, "level": "Bronze", "quiz_results": [], "comp_entries": [], "history": [],
            }
            added += 1
    save(data)
    print(f"Imported {added} promoter(s) from {args[0]}.")


# ── New Tool 24: export (full JSON dump) ─────────────────────────────────────

def cmd_export_all(data: dict) -> None:
    from datetime import datetime
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    export_path = Path(__file__).parent / f"full_export_{ts}.json"
    export_path.write_text(json.dumps(data, indent=2))
    print(f"Full data exported to {export_path.name}")


# ── New Tool 25: analytics ───────────────────────────────────────────────────

def cmd_analytics(data: dict) -> None:
    ps = list(data["promoters"].values())
    if not ps:
        print("No data yet.")
        return
    comps = list(data["competitions"].values())
    all_results = [r for p in ps for r in p.get("quiz_results", [])]
    all_entries = [e for c in comps for e in c["entries"]]

    print(f"\n  ══════ TCL Training Analytics Dashboard ══════════════════")
    print(f"\n  PROMOTER OVERVIEW")
    avg_pts = sum(p["points"] for p in ps) / len(ps)
    print(f"  Total         : {len(ps)}")
    print(f"  Avg points    : {avg_pts:.1f}")
    levels_count = {}
    for p in ps:
        levels_count[p["level"]] = levels_count.get(p["level"], 0) + 1
    for lvl, badge in LEVEL_BADGES.items():
        count = levels_count.get(lvl, 0)
        pct = int(count / len(ps) * 100)
        bar = "█" * count + "░" * max(0, 10 - count)
        print(f"  {badge} {lvl:<10} : {count:>3} ({pct:>3}%)  {bar}")

    print(f"\n  QUIZ ANALYTICS")
    if all_results:
        passed = [r for r in all_results if r["passed"]]
        avg_score = int(sum(r["pct"] for r in all_results) / len(all_results))
        print(f"  Total attempts   : {len(all_results)}")
        print(f"  Overall pass rate: {int(len(passed)/len(all_results)*100)}%")
        print(f"  Average score    : {avg_score}%")
        for qid in QUIZ_BANK:
            q_res = [r for r in all_results if r["quiz"] == qid]
            if q_res:
                q_pass = sum(1 for r in q_res if r["passed"])
                print(f"  {qid:<16} : {len(q_res)} attempts, {int(q_pass/len(q_res)*100)}% pass rate")
    else:
        print("  No quiz attempts yet.")

    print(f"\n  COMPETITION ANALYTICS")
    if all_entries:
        avg_score = sum(e["weighted_score"] for e in all_entries) / len(all_entries)
        print(f"  Total competitions: {len(comps)}")
        print(f"  Total entries     : {len(all_entries)}")
        print(f"  Average score     : {avg_score:.2f}/4.00")
    else:
        print("  No competition entries yet.")

    print(f"\n  TOP PERFORMERS")
    medals = {1: "🥇", 2: "🥈", 3: "🥉"}
    for i, p in enumerate(sorted(ps, key=lambda x: x["points"], reverse=True)[:3], 1):
        print(f"  {medals[i]} {p['name']:<22} {p['points']} pts  {LEVEL_BADGES[p['level']]} {p['level']}")
    print(f"\n  {'═'*54}\n")


# ── New Tool 26: store report ────────────────────────────────────────────────

def cmd_store_report(data: dict) -> None:
    stores: dict[str, list] = {}
    for p in data["promoters"].values():
        stores.setdefault(p["store"], []).append(p)
    if not stores:
        print("No promoters registered yet.")
        return
    print(f"\n  ── Store Performance Report ─────────────────────────────")
    for store, promoters in sorted(stores.items()):
        avg_pts = sum(p["points"] for p in promoters) / len(promoters)
        print(f"\n  {store}  ({len(promoters)} promoters, avg {avg_pts:.0f} pts)")
        for p in sorted(promoters, key=lambda x: x["points"], reverse=True):
            badge = LEVEL_BADGES[p["level"]]
            print(f"    {p['id']}  {p['name']:<22}  {p['points']:>5} pts  {badge}")
    print()


# ── New Tool 27: target set ──────────────────────────────────────────────────

def cmd_target_set(data: dict, args: list) -> None:
    if len(args) < 2:
        print("Usage: target set <promoter_id> <target_pts>")
        sys.exit(1)
    pid = args[0].upper()
    try:
        target = int(args[1])
    except ValueError:
        print("Target must be an integer.")
        sys.exit(1)
    p = require_promoter(data, pid)
    p["target"] = target
    save(data)
    print(f"Target set: {p['name']} → {target} pts by end of month.")


# ── New Tool 28: target check ────────────────────────────────────────────────

def cmd_target_check(data: dict) -> None:
    targets = [(p, p["target"]) for p in data["promoters"].values() if "target" in p]
    if not targets:
        print("No targets set. Use: target set <promoter_id> <pts>")
        return
    print(f"\n  ── Target Progress ───────────────────────────────────────")
    print(f"  {'Name':<22} {'Pts':>6} / {'Target':>7}  {'Progress':<12}  Status")
    print("  " + "─" * 62)
    for p, target in sorted(targets, key=lambda x: x[0]["points"] / max(x[1], 1), reverse=True):
        pct = int(p["points"] / target * 100) if target > 0 else 0
        bar = "█" * min(pct // 10, 10) + "░" * max(0, 10 - pct // 10)
        status = "✓ MET" if p["points"] >= target else f"{target - p['points']} to go"
        print(f"  {p['name']:<22} {p['points']:>6} / {target:>7}  {bar}  {status}")
    print()


# ── New Tool 29: reset ───────────────────────────────────────────────────────

def cmd_reset_all() -> None:
    print("WARNING: This will permanently delete ALL promoter and competition data!")
    c1 = input("Type RESET to continue: ").strip()
    if c1 != "RESET":
        print("Cancelled.")
        return
    c2 = input("Type CONFIRM to proceed: ").strip()
    if c2 != "CONFIRM":
        print("Cancelled.")
        return
    DATA_FILE.write_text(json.dumps({"promoters": {}, "competitions": {}}, indent=2))
    print("All data has been reset.")


# ── New Tool 30: version ─────────────────────────────────────────────────────

def cmd_version() -> None:
    total_q = sum(len(q["questions"]) for q in QUIZ_BANK.values())
    print(f"\n  TCL Electronics KSA — Promoter Training System")
    print(f"  Version  : 2.0")
    print(f"  Quizzes  : {len(QUIZ_BANK)} built-in  ({total_q} questions total)")
    print(f"  Today    : {TODAY}")
    print(f"  Data     : {DATA_FILE}")
    print()


# ── Main ─────────────────────────────────────────────────────────────────────

USAGE = """
  TCL Electronics KSA — Promoter Training System  v2.0

  PROMOTER MANAGEMENT
    promoter add    <name> <store>        Register a new promoter
    promoter list                         List all promoters
    promoter show   <id>                  Show promoter profile and history
    promoter edit   <id> <field> <value>  Edit name or store (field: name|store)
    promoter delete <id>                  Delete a promoter (with confirmation)
    promoter search <keyword>             Search promoters by name or store
    promoter stats  <id>                  Detailed stats dashboard for a promoter
    promoter export                       Export all promoters to CSV
    promoter top    [n]                   Show top N performers (default: 5)

  QUIZZES
    quiz list                             List available quizzes
    quiz run   <quiz_id> <promoter_id>    Run an interactive quiz
    quiz stats                            Analytics across all promoters
    quiz reset <quiz_id|all> <promo_id>   Reset quiz history for a promoter
    quiz export                           Export all quiz results to CSV
    quiz hard  [quiz_id]                  Practice 5 hard questions
    quiz review <quiz_id>                 Show answer key for a quiz
    quiz bank                             Browse full question bank
      quiz IDs: c7l_bronze · c7l_silver · c7l_gold

  POINTS & COACHING
    points add     <id> <pts> <reason>    Manually award points
    points deduct  <id> <pts> <reason>    Manually deduct points
    points history <id>                   Full points history
    coaching log   <id> <notes>           Log coaching session (+10 pts)

  COMPETITIONS
    comp new     <name>                   Create a new competition
    comp list                             List all competitions
    comp score   <comp_id> <promo_id>     Score a promoter's entry
    comp rank    <comp_id>                Finalize rankings + award points
    comp results <comp_id>                View competition results table
    comp delete  <comp_id>                Delete a competition
    comp export  [comp_id]                Export results to CSV (all or one)
    comp stats                            Overall competition analytics
    comp top                              All-time competition champions

  LEADERBOARD
    leaderboard                           Show ranked standings

  ANALYTICS & REPORTING
    analytics                             Advanced analytics dashboard
    store report                          Performance report by store location
    target set   <id> <pts>               Set a monthly points target
    target check                          Check all targets vs current progress
    report                                Full training summary report

  DATA MANAGEMENT
    backup                                Backup data to timestamped JSON file
    restore [filename]                    Restore from a backup file
    import  <csv_file>                    Import promoters from CSV (Name, Store)
    export                                Full JSON data export
    reset                                 Reset ALL data (double confirmation)
    version                               Show system version and info

  EXAMPLES
    python tcl_training.py promoter add "Ahmed Ali" "Riyadh Mall"
    python tcl_training.py promoter edit P001 store "Jeddah Park"
    python tcl_training.py quiz run c7l_gold P001
    python tcl_training.py quiz hard c7l_silver
    python tcl_training.py points add P001 20 "Sales target hit"
    python tcl_training.py coaching log P001 "Objection handling session"
    python tcl_training.py analytics
    python tcl_training.py store report
    python tcl_training.py target set P001 100
    python tcl_training.py backup
    python tcl_training.py leaderboard
    python tcl_training.py report
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
        # Original 12 tools
        ("promoter", "add"):      lambda: cmd_promoter_add(data, rest),
        ("promoter", "list"):     lambda: cmd_promoter_list(data),
        ("promoter", "show"):     lambda: cmd_promoter_show(data, rest),
        ("quiz",     "list"):     lambda: cmd_quiz_list(),
        ("quiz",     "run"):      lambda: cmd_quiz_run(data, rest),
        ("leaderboard", ""):      lambda: cmd_leaderboard(data),
        ("comp",     "new"):      lambda: cmd_comp_new(data, rest),
        ("comp",     "list"):     lambda: cmd_comp_list(data),
        ("comp",     "score"):    lambda: cmd_comp_score(data, rest),
        ("comp",     "rank"):     lambda: cmd_comp_rank(data, rest),
        ("comp",     "results"):  lambda: cmd_comp_results(data, rest),
        ("report",   ""):         lambda: cmd_report(data),
        # New 30 tools
        ("promoter", "edit"):     lambda: cmd_promoter_edit(data, rest),
        ("promoter", "delete"):   lambda: cmd_promoter_delete(data, rest),
        ("promoter", "search"):   lambda: cmd_promoter_search(data, rest),
        ("promoter", "stats"):    lambda: cmd_promoter_stats(data, rest),
        ("promoter", "export"):   lambda: cmd_promoter_export(data),
        ("promoter", "top"):      lambda: cmd_promoter_top(data, rest),
        ("quiz",     "stats"):    lambda: cmd_quiz_stats(data),
        ("quiz",     "reset"):    lambda: cmd_quiz_reset(data, rest),
        ("quiz",     "export"):   lambda: cmd_quiz_export(data),
        ("quiz",     "hard"):     lambda: cmd_quiz_hard(rest),
        ("quiz",     "review"):   lambda: cmd_quiz_review(rest),
        ("quiz",     "bank"):     lambda: cmd_quiz_bank(),
        ("points",   "add"):      lambda: cmd_points_add(data, rest),
        ("points",   "deduct"):   lambda: cmd_points_deduct(data, rest),
        ("points",   "history"):  lambda: cmd_points_history(data, rest),
        ("coaching", "log"):      lambda: cmd_coaching_log(data, rest),
        ("comp",     "delete"):   lambda: cmd_comp_delete(data, rest),
        ("comp",     "export"):   lambda: cmd_comp_export(data, rest),
        ("comp",     "stats"):    lambda: cmd_comp_stats(data),
        ("comp",     "top"):      lambda: cmd_comp_top(data),
        ("backup",   ""):         lambda: cmd_backup(data),
        ("restore",  ""):         lambda: cmd_restore([sub] + rest if sub else rest),
        ("import",   ""):         lambda: cmd_import_csv(data, [sub] + rest if sub else rest),
        ("export",   ""):         lambda: cmd_export_all(data),
        ("analytics",""):         lambda: cmd_analytics(data),
        ("store",    "report"):   lambda: cmd_store_report(data),
        ("target",   "set"):      lambda: cmd_target_set(data, rest),
        ("target",   "check"):    lambda: cmd_target_check(data),
        ("reset",    ""):         lambda: cmd_reset_all(),
        ("version",  ""):         lambda: cmd_version(),
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
