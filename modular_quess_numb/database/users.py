from modular_quess_numb.database.db import get_connection


def get_user_by_telegram_id(telegram_id: int):
    conn = get_connection()  # коннектимся к базе данных
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, telegram_id, total_games, wins FROM users WHERE telegram_id = ?",
        (telegram_id,)
    )

    user = cursor.fetchone()
    conn.close()
    return user


def create_user(telegram_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO users (telegram_id) VALUES (?)",
        (telegram_id,)
    )

    conn.commit()
    conn.close()


def increment_total_games(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET total_games = total_games + 1
        WHERE id = ?
    """, (user_id,))

    conn.commit()
    conn.close()


def increment_wins(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET wins = wins + 1
        WHERE id = ?
    """, (user_id,))

    conn.commit()
    conn.close()
