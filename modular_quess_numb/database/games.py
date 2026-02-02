from modular_quess_numb.database.db import get_connection

ATTEMPTS = 5


def get_active_game(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, secret_number, attempts_left
        FROM games
        WHERE user_id = ? AND is_active = 1
    """, (user_id,))

    game = cursor.fetchone()
    conn.close()
    return game


def start_new_game(user_id: int, secret_number: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO games (user_id, secret_number, attempts_left, is_active)
        VALUES (?, ?, ?, 1)
    """, (user_id, secret_number, ATTEMPTS))

    conn.commit()
    conn.close()


def finish_game(game_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE games
        SET is_active = 0
        WHERE id = ?
    """, (game_id,))

    conn.commit()
    conn.close()


def decrease_attempts(game_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE games
        SET attempts_left = attempts_left - 1
        WHERE id = ?
    """, (game_id,))

    conn.commit()
    conn.close()
