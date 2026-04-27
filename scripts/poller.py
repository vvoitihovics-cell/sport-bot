"""Cron-driven command handler. Runs every 5 min, processes new messages and button taps."""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import messages as msg
import state as st
import telegram_api as tg

SETS_RE = re.compile(r"^\s*([A-Za-zА-Яа-яёЁ_\-]+)\s+(\d+(?:[.,]\d+)?)\s*[xх*]\s*(\d+)\s*[xх*]\s*(\d+)\s*$")


# === Action handlers (each returns (state, reply_text)) ===

def act_start(s):
    return s, msg.START


def act_tren(s):
    s = st.rollover_if_new_day(s)
    s["training_today"] = True
    s["pending_action"] = None
    session = s["rotation"][s["rotation_index"]]
    main_key = msg.SESSION_SCHEMES[session]["main_key"]
    last = next(
        (e for e in reversed(s.get("sets_log", [])) if e["exercise"] == main_key),
        None,
    )
    return s, msg.session_brief(session, s["current_week"], last_main=last)


def act_done(s):
    s["pending_action"] = None
    if not s.get("training_today"):
        return s, "Сегодня не было 💪 Тренировка. Если всё же тренировался — жми сначала её, потом ✅ Готово."
    session = s["rotation"][s["rotation_index"]]
    s["rotation_index"] = (s["rotation_index"] + 1) % len(s["rotation"])
    next_session = s["rotation"][s["rotation_index"]]
    st.update_streak_on_done(s)
    st.append_log(f"Тренировка <b>{session}</b> завершена. Следующая: <b>{next_session}</b>")
    streak_line = f"\n🔥 Streak: {s['streak']}"
    return s, f"✅ <b>{session}</b> зафиксирована.\nСледующая сессия: <b>{next_session}</b>{streak_line}"


def act_skip(s):
    s["pending_action"] = None
    pending = [k for k, v in s["sent_today"].items() if not v]
    if not pending:
        return s, "На сегодня нет ожидающих напоминаний."
    nxt = pending[0]
    s["sent_today"][nxt] = True
    return s, f"Пропускаю напоминание: <b>{nxt}</b>"


def act_status(s):
    s["pending_action"] = None
    next_session = s["rotation"][s["rotation_index"]]
    return s, msg.status_brief(s, next_session)


def act_baddi(s):
    s["pending_action"] = None
    return s, msg.baddi_full()


def act_weight_prompt(s):
    s["pending_action"] = "weight"
    return s, f"{msg.PROMPT_WEIGHT}\n\n{msg.CANCEL_HINT}"


def act_sets_prompt(s):
    s["pending_action"] = "sets"
    return s, f"{msg.PROMPT_SETS}\n\n{msg.CANCEL_HINT}"


def act_note_prompt(s):
    s["pending_action"] = "note"
    return s, f"{msg.PROMPT_NOTE}\n\n{msg.CANCEL_HINT}"


# === pending_action consumers ===

def consume_weight(s, text):
    try:
        kg = float(text.replace(",", ".").strip())
    except ValueError:
        return s, "Не понял. Введи число, например <code>78.5</code>"
    if not (30 <= kg <= 250):
        return s, "Введи разумное значение в кг (30-250)."
    st.add_weight(s, kg)
    s["pending_action"] = None
    delta, current = st.weight_trend(s, days=7)
    if delta is not None:
        sign = "+" if delta >= 0 else ""
        return s, f"⚖️ Записал <b>{current} кг</b> ({sign}{delta} за неделю)"
    return s, f"⚖️ Записал <b>{current} кг</b>"


def consume_sets(s, text):
    m = SETS_RE.match(text.replace(",", "."))
    if not m:
        return s, ("Не понял формат. Пример: <code>prised 130x5x4</code>\n"
                  "(упражнение, вес кг, повторы, подходы)")
    exercise, weight, reps, sets_n = m.groups()
    weight = float(weight)
    reps = int(reps)
    sets_n = int(sets_n)
    st.add_sets(s, exercise.lower(), weight, reps, sets_n)
    s["pending_action"] = None
    return s, f"📝 Записал: <b>{exercise.lower()}</b> {weight}кг × {reps} × {sets_n}"


def consume_note(s, text):
    st.append_log(f"📋 {text}")
    s["pending_action"] = None
    return s, "📋 Записал в лог."


# === Main loop ===

def main():
    s = st.load()
    s = st.rollover_if_new_day(s)
    offset = s.get("last_update_id", 0) + 1
    updates = tg.get_updates(offset=offset)

    if not updates:
        st.save(s)
        print("poller: no new messages")
        return

    processed = 0
    for u in updates:
        s["last_update_id"] = u["update_id"]
        m = u.get("message")
        if not m or "text" not in m:
            continue
        text = m["text"].strip()
        if not text:
            continue

        # Try button label or command first
        first_token = text.split(maxsplit=1)[0]
        action = msg.BUTTON_TO_ACTION.get(text) or msg.BUTTON_TO_ACTION.get(first_token.lower().split("@")[0])

        if action == "start":
            s, reply = act_start(s)
        elif action == "tren":
            s, reply = act_tren(s)
        elif action == "done":
            s, reply = act_done(s)
        elif action == "skip":
            s, reply = act_skip(s)
        elif action == "status":
            s, reply = act_status(s)
        elif action == "baddi":
            s, reply = act_baddi(s)
        elif action == "weight":
            s, reply = act_weight_prompt(s)
        elif action == "sets":
            s, reply = act_sets_prompt(s)
        elif action == "note":
            s, reply = act_note_prompt(s)
        elif s.get("pending_action") == "weight":
            s, reply = consume_weight(s, text)
        elif s.get("pending_action") == "sets":
            s, reply = consume_sets(s, text)
        elif s.get("pending_action") == "note":
            s, reply = consume_note(s, text)
        elif text.startswith("/"):
            reply = "Неизвестная команда. Жми кнопки ниже или ❓"
        else:
            # Free-form text — save to log (likely weekly check-in answer)
            st.append_log(f"💬 {text}")
            reply = "📝 Записал в лог."

        tg.send(reply)
        processed += 1

    st.save(s)
    print(f"poller: processed {processed} updates")


if __name__ == "__main__":
    main()
