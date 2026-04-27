"""Thin wrapper over Telegram Bot API. HTML parse mode + reply keyboard support."""
import json
import os

import requests

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]
BASE = f"https://api.telegram.org/bot{TOKEN}"

# Persistent reply keyboard shown under input field
MAIN_KEYBOARD = {
    "keyboard": [
        [{"text": "💪 Тренировка"}, {"text": "✅ Готово"}],
        [{"text": "📊 Статус"}, {"text": "💊 БАДы"}],
        [{"text": "⚖️ Вес"}, {"text": "📝 Подход"}],
        [{"text": "📋 Заметка"}, {"text": "⏭ Пропустить"}],
    ],
    "resize_keyboard": True,
    "is_persistent": True,
}


def send(text, reply_markup=None, **kwargs):
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }
    if reply_markup is None:
        reply_markup = MAIN_KEYBOARD
    payload["reply_markup"] = json.dumps(reply_markup, ensure_ascii=False)
    payload.update(kwargs)
    r = requests.post(f"{BASE}/sendMessage", data=payload, timeout=15)
    r.raise_for_status()
    return r.json()


def get_updates(offset=0, timeout=0):
    params = {
        "offset": offset,
        "timeout": timeout,
        "allowed_updates": json.dumps(["message"]),
    }
    r = requests.get(f"{BASE}/getUpdates", params=params, timeout=15 + timeout)
    r.raise_for_status()
    return r.json().get("result", [])
