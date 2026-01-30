from typing import Dict

class Game:
    """Логика одной игры пользователя"""
    def __init__(self, attempts: int = 5):
        from random import randint
        self.secret_number: int = randint(1, 100)
        self.attempts: int = attempts
        self.total_games: int = 0
        self.wins: int = 0
        self.in_game: bool = True

    def check_guess(self, guess: int) -> str:
        """Проверка числа, возвращает результат"""
        if guess == self.secret_number:
            self.wins += 1
            self.total_games += 1
            self.in_game = False
            return "win"
        self.attempts -= 1
        if self.attempts == 0:
            self.total_games += 1
            self.in_game = False
            return "lose"
        return "higher" if guess < self.secret_number else "lower"

# Словарь всех пользователей
users: Dict[int, Game] = {}

def get_game(user_id: int) -> Game:
    """
    Возвращает объект игры пользователя.
    Если пользователя нет в словаре, создаёт нового.
    """
    if user_id not in users:
        users[user_id] = Game()
    return users[user_id]