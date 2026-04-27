"""Message templates, session schemes, button labels. HTML parse mode."""

# Button labels (must match telegram_api.MAIN_KEYBOARD)
BTN_TREN = "💪 Тренировка"
BTN_DONE = "✅ Готово"
BTN_STATUS = "📊 Статус"
BTN_BADDI = "💊 БАДы"
BTN_WEIGHT = "⚖️ Вес"
BTN_SETS = "📝 Подход"
BTN_NOTE = "📋 Заметка"
BTN_SKIP = "⏭ Пропустить"

# Map button label or text command → canonical action
BUTTON_TO_ACTION = {
    BTN_TREN: "tren",
    BTN_DONE: "done",
    BTN_STATUS: "status",
    BTN_BADDI: "baddi",
    BTN_WEIGHT: "weight",
    BTN_SETS: "sets",
    BTN_NOTE: "note",
    BTN_SKIP: "skip",
    "/tren": "tren",
    "/done": "done",
    "/status": "status",
    "/baddi": "baddi",
    "/weight": "weight",
    "/sets": "sets",
    "/note": "note",
    "/log": "note",
    "/skip": "skip",
    "/start": "start",
    "/help": "start",
}


SESSION_SCHEMES = {
    "Upper A": {
        "main": "Жим лёжа со штангой",
        "main_key": "bench",
        "accessories": [
            "Жим стоя 3×6",
            "Тяга штанги в наклоне 3×6",
            "Подтягивания с весом 3×6-8",
            "Жим узким хватом 3×10",
            "Молотки на бицепс 3×10",
        ],
    },
    "Lower A": {
        "main": "Присед со штангой",
        "main_key": "squat",
        "accessories": [
            "Румынская тяга 3×6",
            "Жим ногами 3×10",
            "Сгибания ног лёжа 3×12",
            "Подъём на носки стоя 4×12",
            "Планка 3×60с",
        ],
    },
    "Upper B": {
        "main": "Жим стоя со штангой",
        "main_key": "ohp",
        "accessories": [
            "Подтягивания с весом 4×5",
            "Жим лёжа на наклонной 3×8",
            "Тяга верхнего блока 3×10",
            "Тяга гантели одной рукой 3×10",
            "Подъём штанги на бицепс 3×8",
            "Разгибания на блоке 3×12",
        ],
    },
    "Lower B": {
        "main": "Становая тяга",
        "main_key": "deadlift",
        "accessories": [
            "Фронтальный присед 3×5",
            "Болгарские сплит-приседания 3×8 на ногу",
            "Гиперэкстензия с весом 3×10",
            "Подъём на носки сидя 4×15",
            "Колесо для пресса 3×8",
        ],
    },
}

WEEK_SCHEMES = {
    1: ("4×5", "75% от 1ПМ", "Накопление объёма"),
    2: ("4×4", "80% от 1ПМ", "Интенсификация"),
    3: ("5×3", "85% от 1ПМ", "Пиковый блок"),
    4: ("3×5 @ 60% или тест 1-3 ПМ", "60% / 90-100%", "Деload или тест PR"),
}


# === Reminder messages (sent by dispatcher) ===

def morning():
    return (
        "☀️ <b>Доброе утро!</b> Утренние БАДы:\n"
        "• D3 (3000 МЕ) + K2 (100 мкг) — с жирной едой\n"
        "• Омега-3 (2г EPA+DHA)\n"
        "• Lion's Mane (500 мг)\n\n"
        "<i>Если сегодня в зал — жми 💪 Тренировка.</i>"
    )


def pre_workout(session):
    return (
        "⚡ <b>За 30 мин до тренировки:</b>\n"
        "• Кофеин 150 мг + L-теанин 200 мг\n"
        "• Коллаген 10г + витамин C 500 мг\n\n"
        f"Удачной <b>{session}</b>!"
    )


def post_workout():
    return (
        "💪 <b>После тренировки</b> (с едой):\n"
        "• Креатин моногидрат 5г\n"
        "• Ашваганда KSM-66 300 мг\n\n"
        "<i>Когда закончишь — жми ✅ Готово.</i>"
    )


def bedtime():
    return (
        "🌙 <b>Перед сном:</b>\n"
        "• Магний глицинат 350 мг\n"
        "• Мелатонин 0.5–1 мг (только если плохо засыпаешь)\n\n"
        "<i>Спокойной ночи.</i>"
    )


def hydration():
    return "💧 <b>Вода:</b> 500 мл сейчас."


def weekly_checkin(week):
    return (
        f"📊 <b>Чек-ин за неделю {week} блока</b>\n\n"
        "Ответь одним сообщением:\n"
        "1. Сон (1–10)\n"
        "2. Энергия (1–10)\n"
        "3. Все ли тренировки закрыл?\n"
        "4. Самая сложная сессия?\n"
        "5. Что-то болит?\n\n"
        "<i>Сохраню в лог.</i>"
    )


# === On-demand responses ===

def baddi_full():
    return (
        "<b>💊 Курс БАДов</b>\n\n"
        "<b>☀️ Утром:</b>\n"
        "• D3 3000 МЕ + K2 100 мкг (с жирной едой)\n"
        "• Омега-3 2г EPA+DHA\n"
        "• Lion's Mane 500 мг\n\n"
        "<b>⚡ За 30 мин до трени:</b>\n"
        "• Кофеин 150 мг + L-теанин 200 мг\n"
        "• Коллаген 10г + Витамин C 500 мг\n\n"
        "<b>💪 После трени:</b>\n"
        "• Креатин моногидрат 5г\n"
        "• Ашваганда KSM-66 300 мг\n\n"
        "<b>🌙 Перед сном:</b>\n"
        "• Магний глицинат 350 мг\n"
        "• Мелатонин 0.5–1 мг (по необходимости)\n\n"
        "<i>Полный курс с пояснениями: data/kurs-badov.md</i>"
    )


def session_brief(session, week, last_main=None):
    s = SESSION_SCHEMES[session]
    scheme, intensity, focus = WEEK_SCHEMES.get(week, ("—", "—", "—"))
    accessories = "\n".join(f"  • {a}" for a in s["accessories"])
    last_line = ""
    if last_main:
        last_line = (
            f"\n<i>Прошлый раз: {last_main['weight']}кг × {last_main['reps']} × "
            f"{last_main['sets']} ({last_main['date']})</i>"
        )
    return (
        f"💪 Сегодня <b>{session}</b>\n\n"
        f"<b>Основное:</b> {s['main']} — {scheme} @ {intensity}{last_line}\n"
        f"<i>Фокус недели {week}: {focus}</i>\n\n"
        f"<b>Подсобка:</b>\n{accessories}\n\n"
        "<i>Когда закончишь — жми ✅ Готово.</i>"
    )


def status_brief(state, next_session):
    streak = state.get("streak", 0)
    streak_line = f"\n🔥 Streak: <b>{streak}</b>" if streak > 0 else ""

    from state import weight_trend
    delta, current = weight_trend(state, days=7)
    weight_line = ""
    if current is not None:
        if delta is not None:
            sign = "+" if delta >= 0 else ""
            weight_line = f"\n⚖️ Вес: <b>{current} кг</b> ({sign}{delta} за неделю)"
        else:
            weight_line = f"\n⚖️ Вес: <b>{current} кг</b>"

    return (
        "<b>Статус блока:</b>\n"
        f"• Неделя: {state['current_week']} из 4\n"
        f"• Старт блока: {state['block_start']}\n"
        f"• Следующая сессия: <b>{next_session}</b>\n"
        f"• Тренировка сегодня: {'да' if state['training_today'] else 'нет'}"
        f"{streak_line}{weight_line}"
    )


# === Prompts for pending_action flow ===

PROMPT_WEIGHT = "⚖️ Введи вес тела в кг (например: <code>78.5</code>)"
PROMPT_SETS = (
    "📝 Введи рабочий подход:\n"
    "<code>упражнение вес×повт×подходы</code>\n\n"
    "Например: <code>prised 130x5x4</code>\n"
    "или <code>jim 100x3x5</code>"
)
PROMPT_NOTE = "📋 Что записать в лог? Просто ответь следующим сообщением."

CANCEL_HINT = "<i>(чтобы отменить — жми любую другую кнопку)</i>"

START = (
    "<b>Привет!</b> Я — твой тренировочный помощник.\n\n"
    "Используй кнопки ниже:\n"
    "• 💪 Тренировка — в день тренировки, получишь сессию\n"
    "• ✅ Готово — после тренировки\n"
    "• 📊 Статус — где ты в блоке, streak, вес\n"
    "• 💊 БАДы — что пить и когда\n"
    "• ⚖️ Вес — записать вес тела\n"
    "• 📝 Подход — записать рабочий вес в базе\n"
    "• 📋 Заметка — добавить запись в лог\n"
    "• ⏭ Пропустить — пропустить ближайшее напоминание"
)
