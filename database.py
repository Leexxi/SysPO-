"""
Модуль для работы с базой данных SQLite.
Содержит функции для инициализации БД и CRUD-операций над историей сообщений.
"""

import sqlite3
from datetime import datetime

# Путь к файлу базы данных
DB_PATH = "chat.db"


def get_connection() -> sqlite3.Connection:
    """Возвращает соединение с базой данных с включённой поддержкой Row-объектов."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Создаёт таблицу messages, если она ещё не существует."""
    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id        INTEGER PRIMARY KEY AUTOINCREMENT,
                sender    TEXT    NOT NULL,
                text      TEXT    NOT NULL,
                timestamp TEXT    NOT NULL
            )
            """
        )
        conn.commit()


def get_all_messages() -> list[dict]:
    """Возвращает все сообщения из истории, отсортированные по времени."""
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, sender, text, timestamp FROM messages ORDER BY id ASC"
        ).fetchall()
    return [dict(row) for row in rows]


def add_message(sender: str, text: str, timestamp: str) -> dict:
    """
    Добавляет новое сообщение в базу данных.

    :param sender: отправитель ("user" или "server")
    :param text: текст сообщения
    :param timestamp: дата и время получения сообщения сервером
    :return: словарь с данными сохранённого сообщения
    """
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO messages (sender, text, timestamp) VALUES (?, ?, ?)",
            (sender, text, timestamp),
        )
        conn.commit()
        row_id = cursor.lastrowid
    return {"id": row_id, "sender": sender, "text": text, "timestamp": timestamp}


def clear_history() -> None:
    """Удаляет все сообщения из истории чата."""
    with get_connection() as conn:
        conn.execute("DELETE FROM messages")
        conn.commit()
