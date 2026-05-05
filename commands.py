"""
Модуль обработки команд чата.
Поддерживаемые команды: /help, /time, /expr.
"""

import ast
import operator
from datetime import datetime


# Допустимые операторы для безопасного вычисления выражений
ALLOWED_OPERATORS: dict = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _safe_eval(node: ast.AST) -> float:
    """
    Рекурсивно вычисляет AST-узел, допуская только арифметические операции.
    Выбрасывает ValueError при недопустимых конструкциях.
    """
    if isinstance(node, ast.Constant):
        # Числовые литералы
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Недопустимый литерал")
    elif isinstance(node, ast.BinOp):
        # Бинарные операции (+, -, *, /, **, %)
        op_func = ALLOWED_OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError("Недопустимая операция")
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        return op_func(left, right)
    elif isinstance(node, ast.UnaryOp):
        # Унарные операции (-x, +x)
        op_func = ALLOWED_OPERATORS.get(type(node.op))
        if op_func is None:
            raise ValueError("Недопустимая унарная операция")
        return op_func(_safe_eval(node.operand))
    else:
        raise ValueError("Недопустимое выражение")


def cmd_help() -> str:
    """Возвращает справку по доступным командам."""
    return (
        "<b>Доступные команды:</b>\n\n"
        "<code>/help</code> — показать список команд и описание\n"
        "<code>/time</code> — показать текущее время сервера\n"
        "<code>/expr &lt;выражение&gt;</code> — вычислить математическое выражение\n"
        "     Пример: <code>/expr 2+2*2</code> → 6\n"
        "     Поддерживаются: +, -, *, /, **, %\n\n"
        "Любое другое сообщение будет возвращено эхом."
    )


def cmd_time() -> str:
    """Возвращает текущее время сервера."""
    now = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
    return f"Текущее время сервера: <b>{now}</b>"


def cmd_expr(args: str) -> str:
    """
    Вычисляет математическое выражение из строки args.
    Использует безопасный AST-парсер вместо eval().

    :param args: строка с выражением, например "2+2*2"
    :return: результат вычисления или сообщение об ошибке
    """
    expr = args.strip()
    if not expr:
        return "Укажите выражение. Пример: <code>/expr 2+2*2</code>"
    try:
        tree = ast.parse(expr, mode="eval")
        result = _safe_eval(tree.body)
        # Отображаем целое число, если результат — целый
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return f"<code>{expr}</code> = <b>{result}</b>"
    except ZeroDivisionError:
        return "Ошибка: деление на ноль"
    except (ValueError, TypeError, SyntaxError):
        return f"Не удалось вычислить выражение: <code>{expr}</code>"


def handle_command(text: str) -> str | None:
    """
    Определяет, является ли text командой, и выполняет её.

    :param text: входной текст пользователя
    :return: ответ сервера на команду, либо None если text — не команда
    """
    stripped = text.strip()
    if not stripped.startswith("/"):
        return None

    # Разбиваем на имя команды и аргументы
    parts = stripped.split(maxsplit=1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ""

    if command == "/help":
        return cmd_help()
    elif command == "/time":
        return cmd_time()
    elif command == "/expr":
        return cmd_expr(args)
    else:
        return f"Неизвестная команда: <code>{command}</code>. Введите <code>/help</code> для справки."
