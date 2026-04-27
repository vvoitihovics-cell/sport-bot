"""Cron-driven dispatcher. Runs every 15 min, sends reminder if a slot matches now."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import messages as msg
import state as st
import telegram_api as tg

WINDOW_MIN = 7

# (slot_name, hour, minute, predicate(state, now))
SLOTS = [
    ("morning", 6, 45, lambda s, now: True),
    ("pre_workout", 7, 30, lambda s, now: s.get("training_today", False)),
    ("post_workout", 9, 30, lambda s, now: s.get("training_today", False)),
    ("hydration_12", 12, 0, lambda s, now: True),
    ("hydration_16", 16, 0, lambda s, now: True),
    ("weekly_checkin", 19, 0, lambda s, now: now.weekday() == 6),  # Sunday
    ("bedtime", 22, 30, lambda s, now: True),
]


def main():
    s = st.load()
    s = st.rollover_if_new_day(s)
    now = st.now_local(s)

    fired = None
    for slot, hh, mm, predicate in SLOTS:
        target = now.replace(hour=hh, minute=mm, second=0, microsecond=0)
        diff_min = abs((now - target).total_seconds()) / 60
        if diff_min > WINDOW_MIN:
            continue
        if s["sent_today"].get(slot):
            continue
        if not predicate(s, now):
            continue

        if slot == "morning":
            tg.send(msg.morning())
        elif slot == "pre_workout":
            session = s["rotation"][s["rotation_index"]]
            tg.send(msg.pre_workout(session))
        elif slot == "post_workout":
            tg.send(msg.post_workout())
        elif slot == "bedtime":
            tg.send(msg.bedtime())
        elif slot in ("hydration_12", "hydration_16"):
            tg.send(msg.hydration())
        elif slot == "weekly_checkin":
            tg.send(msg.weekly_checkin(s["current_week"]))

        s["sent_today"][slot] = True
        fired = slot
        break

    st.save(s)
    print(f"dispatcher: fired={fired} time={now.strftime('%Y-%m-%d %H:%M %Z')}")


if __name__ == "__main__":
    main()
