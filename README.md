# sport-bot

Telegram-бот для напоминаний о БАДах и тренировках. Работает на GitHub Actions, без своего сервера.

## Что делает

| Когда (Europe/Riga) | Что присылает |
|---|---|
| Каждый день 06:45 | Утренние БАДы (D3+K2, омега-3, Lion's Mane) |
| 07:30, если жали 💪 Тренировка | Пре-воркаут (кофеин+L-теанин, коллаген+C) |
| 09:30, если жали 💪 Тренировка | Пост-воркаут (креатин, ашваганда) |
| 12:00 и 16:00 | Напоминание попить воду |
| Каждый день 22:30 | Перед сном (магний глицинат) |
| Воскресенье 19:00 | Еженедельный чек-ин |

## Кнопки бота

В Telegram под полем ввода всегда видны 8 кнопок:

| Кнопка | Что делает |
|---|---|
| 💪 Тренировка | Пометить сегодня тренировочным, получить сессию (Upper A / Lower A / …) и схему базы по неделе |
| ✅ Готово | Тренировка завершена, ротация двигается на следующую сессию, увеличивается streak |
| 📊 Статус | Текущая неделя блока, следующая сессия, streak, тренд веса |
| 💊 БАДы | Полный список БАДов по времени дня |
| ⚖️ Вес | Записать текущий вес тела (бот спросит число) |
| 📝 Подход | Записать рабочий подход в формате `упражнение вес×повт×подходы` |
| 📋 Заметка | Добавить произвольную запись в лог |
| ⏭ Пропустить | Пропустить ближайшее напоминание |

Старые типизированные команды (`/tren`, `/done`, `/status`, `/baddi`, `/weight`, `/sets`, `/note`, `/skip`) тоже работают для совместимости.

---

## Настройка (один раз, ~10 минут)

### Шаг 1. Зарегистрируй GitHub
1. Зайди на https://github.com/signup
2. Создай аккаунт, подтверди email

### Шаг 2. Создай Telegram-бота
1. В Telegram открой чат с **@BotFather** (https://t.me/BotFather)
2. Напиши `/newbot`
3. Введи имя бота (любое, например `Sport Coach`)
4. Введи username (должен заканчиваться на `bot`, например `viktor_sport_bot`)
5. **Сохрани токен** который выдаст BotFather — выглядит как `1234567890:AAExxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Шаг 3. Узнай свой `chat_id`
1. Найди своего бота в Telegram (по username из шага 2) и напиши ему любое сообщение, например `start`
2. Открой в браузере (подставь свой токен): `https://api.telegram.org/bot<ТВОЙ_ТОКЕН>/getUpdates`
3. В JSON найди `"chat":{"id":123456789,...}` — это твой `chat_id`. Сохрани его

### Шаг 4. Создай репозиторий на GitHub
1. На github.com нажми `+` (правый верхний угол) → **New repository**
2. Имя: `sport-bot`
3. **Public** (важно — для приватных Actions имеют лимиты)
4. **Не** ставь галочки на README/gitignore (всё уже есть в этой папке)
5. Нажми **Create repository**

### Шаг 5. Добавь секреты в репозиторий
1. В репо: **Settings** → **Secrets and variables** → **Actions** → **New repository secret**
2. Создай два секрета:
   - Name: `TELEGRAM_BOT_TOKEN`, Value: токен из шага 2
   - Name: `TELEGRAM_CHAT_ID`, Value: chat_id из шага 3

### Шаг 6. Загрузи код в репозиторий

В терминале:

```bash
cd ~/Desktop/sport-bot
git init
git add .
git commit -m "initial: sport bot"
git branch -M main
git remote add origin https://github.com/<ТВОЙ_USERNAME>/sport-bot.git
git push -u origin main
```

Замени `<ТВОЙ_USERNAME>` на свой логин GitHub.

При первом push GitHub попросит авторизацию — используй **Personal Access Token** вместо пароля:
1. На GitHub: **Settings** (профиль) → **Developer settings** → **Personal access tokens** → **Tokens (classic)** → **Generate new token (classic)**
2. Note: `sport-bot push`, Expiration: 90 days, Scopes: ✓ `repo`
3. Скопируй токен и используй его как пароль при `git push`

### Шаг 7. Тест
1. На GitHub в репо открой вкладку **Actions**
2. Найди workflow **poll**, нажми **Run workflow** → **Run workflow** (зелёная кнопка)
3. Подожди 30 секунд
4. В Telegram напиши боту `/start` — должен прийти список команд
5. Напиши `/tren` — должна прийти сегодняшняя сессия с подсобкой

---

## Структура проекта

```
sport-bot/
├── .github/workflows/
│   ├── reminders.yml    # cron */15 3-21 * * * (UTC) — напоминания
│   └── poll.yml         # cron */5 * * * * — обработка команд
├── scripts/
│   ├── dispatcher.py    # отправляет напоминание если совпало время
│   ├── poller.py        # обрабатывает входящие команды
│   ├── messages.py      # тексты напоминаний и схемы тренировок
│   ├── state.py         # чтение/запись state, daily rollover
│   └── telegram_api.py  # обёртка над Telegram Bot API
├── state/
│   ├── current.json     # состояние (неделя, ротация, флаги отправки)
│   └── log.md           # лог чек-инов и заметок
├── data/
│   ├── plan-trenirovok.md   # копия тренировочного плана
│   └── kurs-badov.md        # копия курса БАДов
├── requirements.txt
└── README.md
```

## Как меняется блок

После 4 недель блок заканчивается. Чтобы начать новый:
1. Открой `state/current.json` в репо (через веб-редактор GitHub)
2. Поменяй `block_start` на новую дату (например, понедельник следующей недели)
3. Поставь `current_week: 1`, `rotation_index: 0`
4. Сохрани (Commit changes)

## Если что-то пошло не так

- **Бот не отвечает** → Settings → Secrets, проверь `TELEGRAM_BOT_TOKEN` и `TELEGRAM_CHAT_ID`
- **Workflow падает с git push error** → проверь, что репо public и Actions включены (Settings → Actions → General → Allow all)
- **Напоминания не приходят** → открой Actions, посмотри последний run `reminders` — там логи
- **Перерыв в тренировках** → ничего не делай, бот ждёт `/tren`

## Лимиты GitHub Actions

Repo public → лимитов нет. Расход:
- `reminders`: 4×18 = 72 запуска/день (по 30 сек)
- `poll`: 12×24 = 288 запусков/день (по 15 сек)
- Итого ~110 минут/день, бесплатно для публичных репо
