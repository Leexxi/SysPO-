# Chat WebApp

Простое веб-приложение чата, реализованное на **FastAPI** (бэкенд), чистом **HTML/CSS/JS** (фронтенд) и **SQLite** (база данных).

## Возможности

- Чат с сервером в реальном времени
- История сообщений сохраняется в базе данных и загружается при перезапуске
- Кнопка очистки всей истории (с подтверждением)
- Каждое сообщение помечается датой и временем получения сервером
- Современный тёмный интерфейс

## Поддерживаемые команды

| Команда | Описание |
|---|---|
| `/help` | Список всех команд |
| `/time` | Текущее время сервера |
| `/expr <выражение>` | Вычисление математического выражения |

**Примеры `/expr`:**
```
/expr 2+2*2       → 6
/expr (10-4)/2    → 3
/expr 2**8        → 256
/expr 17%5        → 2
```

## Структура проекта

```
SysPO/
├── main.py          # FastAPI-приложение, маршруты
├── database.py      # Работа с SQLite
├── commands.py      # Обработчики команд
├── schemas.py       # Pydantic-схемы
├── templates/
│   └── index.html   # Страница чата
├── static/
│   ├── style.css    # Стили
│   └── app.js       # Логика фронтенда
├── requirements.txt # Зависимости
└── README.md
```

## Установка и запуск

### 0. Требования

#### Python 3.10+

Приложение требует Python версии **3.10 или выше**.

**macOS / Linux** (через [pyenv](https://github.com/pyenv/pyenv), рекомендуется):
```bash
brew install pyenv           # macOS (Homebrew)
pyenv install 3.12.2
pyenv global 3.12.2
```

Или скачайте установщик напрямую с официального сайта: https://www.python.org/downloads/

Проверьте установку:
```bash
python3 --version
```

**Windows:**

Скачайте установщик `.exe` с https://www.python.org/downloads/ и запустите его.
При установке обязательно поставьте галочку **"Add Python to PATH"**.

Проверьте установку:
```cmd
python --version
```

#### SQLite

SQLite **не требует отдельной установки** — модуль `sqlite3` входит в стандартную библиотеку Python.
База данных `chat.db` будет создана автоматически при первом запуске сервера.

Если вы хотите работать с базой данных напрямую через консоль, SQLite CLI можно установить так:

**macOS:**
```bash
brew install sqlite
```

**Linux (Debian/Ubuntu):**
```bash
sudo apt install sqlite3
```

**Windows:**

Скачайте `sqlite-tools-win32-*.zip` с https://sqlite.org/download.html и добавьте папку в PATH.

После установки можно просмотреть содержимое базы командой:
```bash
sqlite3 chat.db "SELECT * FROM messages;"
```

---

### 1. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 2. Запуск сервера

```bash
uvicorn main:app --reload
```

### 3. Открыть в браузере

```
http://localhost:8000
```

## API

| Метод | Путь | Описание |
|---|---|---|
| `GET` | `/` | Страница чата |
| `GET` | `/api/history` | Вся история сообщений |
| `POST` | `/api/message` | Отправить сообщение |
| `DELETE` | `/api/history` | Очистить историю |

### Пример запроса `POST /api/message`
```json
{ "text": "/expr 2+2" }
```

### Пример ответа
```json
{
  "user_message":   { "id": 1, "sender": "user",   "text": "/expr 2+2", "timestamp": "14.04.2026 10:00:00" },
  "server_message": { "id": 2, "sender": "server", "text": "<code>2+2</code> = <b>4</b>", "timestamp": "14.04.2026 10:00:00" }
}
```

## Технологии

- [FastAPI](https://fastapi.tiangolo.com/) — веб-фреймворк
- [Uvicorn](https://www.uvicorn.org/) — ASGI-сервер
- [Jinja2](https://jinja.palletsprojects.com/) — HTML-шаблоны
- SQLite (стандартная библиотека Python `sqlite3`) — база данных
