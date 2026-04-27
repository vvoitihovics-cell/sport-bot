# sport-bot

> ℹ️ **Этот код переехал на Cloudflare Workers.** Текущий рабочий код в `~/Desktop/sport-bot-worker/`. Полная история (включая старую Python-реализацию на GitHub Actions) — в git log.

Тренировочный бот в Telegram, работающий на Cloudflare Workers с webhook'ом — мгновенный ответ на любую кнопку (< 1 сек).

## Что бот делает

| Когда (Europe/Riga) | Что присылает |
|---|---|
| 06:45 каждый день | Утренние БАДы |
| 07:30 в дни 💪 Тренировка | Пре-воркаут |
| 09:30 в дни 💪 Тренировка | Пост-воркаут |
| 12:00, 16:00 | 💧 Вода |
| 22:30 | Перед сном (магний) |
| Воскресенье 19:00 | Еженедельный чек-ин |

## Кнопки

💪 Тренировка / ✅ Готово / 📊 Статус / 💊 БАДы /
⚖️ Вес / 📝 Подход / 📋 Заметка / ⏭ Пропустить

## Архитектура

- **Cloudflare Worker** (`sport-bot.vvoitihovics-cell.workers.dev`) — webhook + cron
- **KV** хранит state (`state` ключ) и лог (`log` ключ)
- **Cron** триггер каждые 15 мин с 03:00 до 21:00 UTC, выбирает слот по локальному времени Europe/Riga

## Деплой

Код Worker'a в `~/Desktop/sport-bot-worker/`. Полная инструкция — в `sport-bot-worker/README.md`.

```bash
cd ~/Desktop/sport-bot-worker
npm install
wrangler deploy
```
