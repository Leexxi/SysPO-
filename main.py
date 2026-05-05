"""
Главный модуль FastAPI-приложения.
Определяет маршруты API и подключает статические файлы и шаблоны.
"""

from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from commands import handle_command
from database import add_message, clear_history, get_all_messages, init_db
from schemas import MessageOut, MessageRequest, SendMessageResponse

# Инициализация приложения
app = FastAPI(title="Chat WebApp")

# Подключение статических файлов (CSS, JS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Подключение шаблонов Jinja2
templates = Jinja2Templates(directory="templates")


@app.on_event("startup")
def startup_event() -> None:
    """Инициализация базы данных при запуске сервера."""
    init_db()


# ──────────────────────────────────────────────────────────────────────────────
# Страницы
# ──────────────────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    """Отдаёт единственную HTML-страницу чата."""
    return templates.TemplateResponse("index.html", {"request": request})


# ──────────────────────────────────────────────────────────────────────────────
# REST API
# ──────────────────────────────────────────────────────────────────────────────

@app.get("/api/history", response_model=list[MessageOut])
def get_history() -> list[dict]:
    """Возвращает всю историю сообщений из базы данных."""
    return get_all_messages()


@app.post("/api/message", response_model=SendMessageResponse)
def send_message(payload: MessageRequest) -> dict:
    """
    Обрабатывает сообщение пользователя:
    1. Сохраняет сообщение пользователя в БД с отметкой времени сервера.
    2. Определяет ответ: команда или эхо.
    3. Сохраняет ответ сервера в БД.
    4. Возвращает оба сообщения клиенту.
    """
    # Получаем текущее время сервера в момент получения сообщения
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    # Сохраняем сообщение пользователя
    user_msg = add_message(sender="user", text=payload.text, timestamp=now)

    # Формируем ответ сервера: команда или эхо
    command_result = handle_command(payload.text)
    server_text = command_result if command_result is not None else f"Эхо: {payload.text}"

    # Сохраняем ответ сервера
    server_msg = add_message(sender="server", text=server_text, timestamp=now)

    return {"user_message": user_msg, "server_message": server_msg}


@app.delete("/api/history")
def delete_history() -> dict:
    """Очищает всю историю сообщений из базы данных."""
    clear_history()
    return {"status": "ok", "message": "История очищена"}
