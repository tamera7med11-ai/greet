# TCL Electronics KSA — Promoter Training System

A CLI toolkit for managing promoter product knowledge, quiz assessments, competition scoring, and leaderboard rankings.

---

## Tools

| File | Purpose |
|---|---|
| `tcl_training.py` | Main training system (quiz, tracker, leaderboard, competition, report) |
| `training_tracker.py` | Personal June 2026 monthly training plan tracker |
| `TCL_Training_System_Framework.md` | Full system blueprint and implementation roadmap |

---

## Quick Start

```bash
# Register promoters
python tcl_training.py promoter add "Ahmed Ali" "Riyadh Mall"
python tcl_training.py promoter list

# Run a quiz
python tcl_training.py quiz list
python tcl_training.py quiz run c7l_bronze P001
python tcl_training.py quiz run c7l_silver P001
python tcl_training.py quiz run c7l_gold   P001

# View leaderboard
python tcl_training.py leaderboard

# Run a competition
python tcl_training.py comp new "C7L Mastery Phase 1"
python tcl_training.py comp score C001 P001
python tcl_training.py comp rank  C001
python tcl_training.py comp results C001

# Full report
python tcl_training.py report
```

---

## Quiz Bank

| ID | Level | Questions | Pass |
|---|---|---|---|
| `c7l_bronze` | Bronze | 10 | 70% |
| `c7l_silver` | Silver | 15 | 75% |
| `c7l_gold`   | Gold   | 20 | 85% |

---

## Points & Levels

| Activity | Points |
|---|---|
| Bronze quiz pass | +10 |
| Silver quiz pass | +20 |
| Gold quiz pass | +35 |
| Perfect score bonus | +5 |
| Competition submission | +15 |
| 1st place | +25 |
| 2nd place | +15 |
| 3rd place | +10 |

| Level | Points |
|---|---|
| 🥉 Bronze | 0–49 |
| 🥈 Silver | 50–99 |
| 🥇 Gold | 100–149 |
| 🏆 Champion | 150+ |

---

## Monthly Training Tracker

```bash
python training_tracker.py list
python training_tracker.py done  w2d2
python training_tracker.py skip  w2d3
python training_tracker.py undo  w2d2
python training_tracker.py add   "Jun 15" "Extra session"
```

---

## Requirements

Python 3.10+
