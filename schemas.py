"""
Pydantic-схемы для валидации входящих запросов и формирования ответов API.
"""

from pydantic import BaseModel


class MessageRequest(BaseModel):
    """Схема входящего сообщения от пользователя."""
    text: str


class MessageOut(BaseModel):
    """Схема одного сообщения для передачи на фронтенд."""
    id: int
    sender: str   # "user" или "server"
    text: str
    timestamp: str


class SendMessageResponse(BaseModel):
    """Ответ API при отправке сообщения: пара (сообщение пользователя, ответ сервера)."""
    user_message: MessageOut
    server_message: MessageOut
