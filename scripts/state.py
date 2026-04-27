"""State management — JSON file with daily rollover, weekly tracking, logs."""
import datetime
import json
from pathlib import Path

import pytz

ROOT = Path(__file__).resolve().parent.parent
STATE_FILE = ROOT / "state" / "current.json"
LOG_FILE = ROOT / "state" / "log.md"

DEFAULT_SENT_TODAY = {
    "morning": False,
    "pre_workout": False,
    "post_workout": False,
    "bedtime": False,
    "weekly_checkin": False,
    "hydration_12": False,
    "hydration_16": False,
}


def load():
    s = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    return _migrate(s)


def _migrate(s):
    """Ensure every expected field exists with a default."""
    s.setdefault("pending_action", None)
    s.setdefault("streak", 0)
    s.setdefault("last_done_date", None)
    s.setdefault("weight_log", [])
    s.setdefault("sets_log", [])
    sent = s.setdefault("sent_today", {})
    for k, v in DEFAULT_SENT_TODAY.items():
        sent.setdefault(k, v)
    return s


def save(state):
    STATE_FILE.write_text(
        json.dumps(state, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def now_local(state):
    return datetime.datetime.now(pytz.timezone(state["tz"]))


def today_local(state):
    return now_local(state).date().isoformat()


def update_week(state):
    today = datetime.date.fromisoformat(today_local(state))
    start = datetime.date.fromisoformat(state["block_start"])
    days_in = (today - start).days
    state["current_week"] = 1 if days_in < 0 else min(4, days_in // 7 + 1)
    return state


def rollover_if_new_day(state):
    today = today_local(state)
    if state.get("today_date") != today:
        state["today_date"] = today
        state["training_today"] = False
        state["sent_today"] = {k: False for k in DEFAULT_SENT_TODAY}
    update_week(state)
    return state


def append_log(text):
    now = datetime.datetime.now(pytz.timezone("Europe/Riga")).strftime("%Y-%m-%d %H:%M")
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(f"\n## {now}\n{text}\n")


def add_weight(state, kg):
    state["weight_log"].append({"date": today_local(state), "kg": kg})


def add_sets(state, exercise, weight, reps, sets_n):
    state["sets_log"].append({
        "date": today_local(state),
        "exercise": exercise,
        "weight": weight,
        "reps": reps,
        "sets": sets_n,
    })


def update_streak_on_done(state):
    today = datetime.date.fromisoformat(today_local(state))
    last = state.get("last_done_date")
    if last:
        gap = (today - datetime.date.fromisoformat(last)).days
        state["streak"] = state.get("streak", 0) + 1 if 0 < gap <= 3 else 1
    else:
        state["streak"] = 1
    state["last_done_date"] = today.isoformat()


def weight_trend(state, days=7):
    """Return (kg_delta, current_kg) over last N days, or (None, None) if insufficient data."""
    log = state.get("weight_log", [])
    if not log:
        return None, None
    today = datetime.date.fromisoformat(today_local(state))
    cutoff = today - datetime.timedelta(days=days)
    older = [e for e in log if datetime.date.fromisoformat(e["date"]) <= cutoff]
    current = log[-1]["kg"]
    if not older:
        return None, current
    return round(current - older[-1]["kg"], 2), current
