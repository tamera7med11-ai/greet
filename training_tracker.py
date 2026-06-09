#!/usr/bin/env python3
"""Monthly training plan tracker for June 2026."""

import json
import sys
from datetime import date
from pathlib import Path

DATA_FILE = Path(__file__).parent / "training_data.json"
TODAY = date.today()
MONTH = "June 2026"

STATUS_DONE = "done"
STATUS_TODO = "todo"
STATUS_SKIP = "skip"

ICONS = {STATUS_DONE: "[x]", STATUS_TODO: "[ ]", STATUS_SKIP: "[-]"}


def load_data() -> dict:
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return _default_plan()


def save_data(data: dict) -> None:
    DATA_FILE.write_text(json.dumps(data, indent=2))


def _default_plan() -> dict:
    weeks = [
        {
            "week": 1,
            "label": "Foundation (Jun 1–7)",
            "tasks": [
                {"id": "w1d1", "day": "Mon Jun 1",  "name": "Full-body strength – 3×10 squats, push-ups, rows",    "status": STATUS_DONE},
                {"id": "w1d2", "day": "Tue Jun 2",  "name": "30-min steady-state cardio (run/cycle)",              "status": STATUS_DONE},
                {"id": "w1d3", "day": "Wed Jun 3",  "name": "Core & mobility – planks, hip flexor stretches",      "status": STATUS_DONE},
                {"id": "w1d4", "day": "Thu Jun 4",  "name": "Upper body – bench press, overhead press, pull-ups",  "status": STATUS_DONE},
                {"id": "w1d5", "day": "Fri Jun 5",  "name": "Lower body – deadlifts, lunges, calf raises",         "status": STATUS_DONE},
                {"id": "w1d6", "day": "Sat Jun 6",  "name": "Active recovery – 45-min walk or yoga",               "status": STATUS_DONE},
                {"id": "w1d7", "day": "Sun Jun 7",  "name": "Rest day",                                            "status": STATUS_DONE},
            ],
        },
        {
            "week": 2,
            "label": "Building (Jun 8–14)",
            "tasks": [
                {"id": "w2d1", "day": "Mon Jun 8",  "name": "Full-body strength – increase weight 5%",             "status": STATUS_DONE},
                {"id": "w2d2", "day": "Tue Jun 9",  "name": "Interval cardio – 6×3-min hard / 2-min easy",        "status": STATUS_TODO},
                {"id": "w2d3", "day": "Wed Jun 10", "name": "Core circuit – 4 rounds: hollow hold, dead bug, RKC", "status": STATUS_TODO},
                {"id": "w2d4", "day": "Thu Jun 11", "name": "Upper body – add 1 set per exercise",                 "status": STATUS_TODO},
                {"id": "w2d5", "day": "Fri Jun 12", "name": "Lower body – add 1 set per exercise",                 "status": STATUS_TODO},
                {"id": "w2d6", "day": "Sat Jun 13", "name": "Hike or long bike ride (60 min)",                     "status": STATUS_TODO},
                {"id": "w2d7", "day": "Sun Jun 14", "name": "Rest day",                                            "status": STATUS_TODO},
            ],
        },
        {
            "week": 3,
            "label": "Intensity (Jun 15–21)",
            "tasks": [
                {"id": "w3d1", "day": "Mon Jun 15", "name": "Full-body HIIT – 20 min Tabata",                      "status": STATUS_TODO},
                {"id": "w3d2", "day": "Tue Jun 16", "name": "Tempo run – 5 km at comfortably hard pace",           "status": STATUS_TODO},
                {"id": "w3d3", "day": "Wed Jun 17", "name": "Yoga / deep stretch (45 min)",                        "status": STATUS_TODO},
                {"id": "w3d4", "day": "Thu Jun 18", "name": "Push day – chest, shoulders, triceps 4×8",            "status": STATUS_TODO},
                {"id": "w3d5", "day": "Fri Jun 19", "name": "Pull day – back, biceps, rear delts 4×8",             "status": STATUS_TODO},
                {"id": "w3d6", "day": "Sat Jun 20", "name": "Leg day – heavy squats & RDLs 4×6",                   "status": STATUS_TODO},
                {"id": "w3d7", "day": "Sun Jun 21", "name": "Rest day",                                            "status": STATUS_TODO},
            ],
        },
        {
            "week": 4,
            "label": "Peak (Jun 22–28)",
            "tasks": [
                {"id": "w4d1", "day": "Mon Jun 22", "name": "Max-effort full-body circuit – 5 rounds",             "status": STATUS_TODO},
                {"id": "w4d2", "day": "Tue Jun 23", "name": "Long run – 8 km at easy pace",                        "status": STATUS_TODO},
                {"id": "w4d3", "day": "Wed Jun 24", "name": "Core & stability – single-leg work, pallof press",    "status": STATUS_TODO},
                {"id": "w4d4", "day": "Thu Jun 25", "name": "Upper body strength test – max reps benchmark",       "status": STATUS_TODO},
                {"id": "w4d5", "day": "Fri Jun 26", "name": "Lower body strength test – 1RM squat & deadlift",     "status": STATUS_TODO},
                {"id": "w4d6", "day": "Sat Jun 27", "name": "Active recovery swim or cycle (45 min)",              "status": STATUS_TODO},
                {"id": "w4d7", "day": "Sun Jun 28", "name": "Rest day",                                            "status": STATUS_TODO},
            ],
        },
        {
            "week": 5,
            "label": "Recovery (Jun 29–30)",
            "tasks": [
                {"id": "w5d1", "day": "Mon Jun 29", "name": "Light full-body movement – 50% intensity",            "status": STATUS_TODO},
                {"id": "w5d2", "day": "Tue Jun 30", "name": "End-of-month review + mobility session",              "status": STATUS_TODO},
            ],
        },
    ]
    return {"month": MONTH, "weeks": weeks}


def all_tasks(data: dict) -> list[dict]:
    return [t for w in data["weeks"] for t in w["tasks"]]


def find_task(data: dict, task_id: str) -> dict | None:
    return next((t for t in all_tasks(data) if t["id"] == task_id), None)


def cmd_list(data: dict) -> None:
    tasks = all_tasks(data)
    done = sum(1 for t in tasks if t["status"] == STATUS_DONE)
    total = len(tasks)
    pct = int(done / total * 100)

    print(f"\n  Training Plan — {data['month']}")
    print(f"  Progress: {done}/{total} tasks complete ({pct}%)\n")

    for week in data["weeks"]:
        print(f"  Week {week['week']}: {week['label']}")
        for t in week["tasks"]:
            icon = ICONS[t["status"]]
            today_marker = " ← today" if TODAY.strftime("%b %-d") in t["day"] and TODAY.month == 6 else ""
            print(f"    {icon} {t['id']:5}  {t['day']:12}  {t['name']}{today_marker}")
        print()


def cmd_done(data: dict, task_id: str) -> None:
    task = find_task(data, task_id)
    if not task:
        print(f"Task '{task_id}' not found. Run 'list' to see valid IDs.")
        sys.exit(1)
    task["status"] = STATUS_DONE
    save_data(data)
    print(f"Marked {task_id} as done: {task['name']}")


def cmd_undo(data: dict, task_id: str) -> None:
    task = find_task(data, task_id)
    if not task:
        print(f"Task '{task_id}' not found.")
        sys.exit(1)
    task["status"] = STATUS_TODO
    save_data(data)
    print(f"Reset {task_id} to todo: {task['name']}")


def cmd_skip(data: dict, task_id: str) -> None:
    task = find_task(data, task_id)
    if not task:
        print(f"Task '{task_id}' not found.")
        sys.exit(1)
    task["status"] = STATUS_SKIP
    save_data(data)
    print(f"Marked {task_id} as skipped: {task['name']}")


def cmd_add(data: dict, day: str, name: str) -> None:
    last_week = data["weeks"][-1]
    existing_ids = {t["id"] for t in all_tasks(data)}
    n = len(all_tasks(data)) + 1
    new_id = f"extra{n}"
    while new_id in existing_ids:
        n += 1
        new_id = f"extra{n}"
    task = {"id": new_id, "day": day, "name": name, "status": STATUS_TODO}
    last_week["tasks"].append(task)
    save_data(data)
    print(f"Added task {new_id}: [{day}] {name}")


def usage() -> None:
    print(
        f"""
  Training Tracker — {MONTH}

  Usage:
    python training_tracker.py list
    python training_tracker.py done  <id>        # mark task complete
    python training_tracker.py undo  <id>        # reset to todo
    python training_tracker.py skip  <id>        # mark as skipped
    python training_tracker.py add   <day> <task description>

  Examples:
    python training_tracker.py list
    python training_tracker.py done w2d2
    python training_tracker.py add "Wed Jun 10" "Extra stretching session"
"""
    )


def main() -> None:
    data = load_data()
    args = sys.argv[1:]

    if not args or args[0] in ("-h", "--help", "help"):
        usage()
        return

    cmd = args[0]

    if cmd == "list":
        cmd_list(data)
    elif cmd == "done" and len(args) == 2:
        cmd_done(data, args[1])
    elif cmd == "undo" and len(args) == 2:
        cmd_undo(data, args[1])
    elif cmd == "skip" and len(args) == 2:
        cmd_skip(data, args[1])
    elif cmd == "add" and len(args) >= 3:
        cmd_add(data, args[1], " ".join(args[2:]))
    else:
        print(f"Unknown command or wrong number of arguments: {' '.join(args)}")
        usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
