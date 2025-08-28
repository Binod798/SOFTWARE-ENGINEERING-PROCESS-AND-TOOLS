import random

WORDS = [
    "python", "java", "linux", "docker", "git",
    "cloud", "api", "debug", "server", "binary"
]

PHRASES = [
    "machine learning",
    "artificial intelligence",
    "software engineering",
    "data science",
    "open source",
    "computer network",
    "object oriented programming",
    "operating system",
    "cloud computing",
    "version control"
]


class HangmanLogic:
    def __init__(self, mode="basic", lives=6):
        self.lives = lives
        if mode == "basic":
            self.word = random.choice(WORDS).lower()
        elif mode == "intermediate":
            self.word = random.choice(PHRASES).lower()
        else:
            raise ValueError("Invalid mode")
        self.display = ["_" if c != " " else " " for c in self.word]

    def guess(self, letter: str):
        if letter in self.word:
            for i, ch in enumerate(self.word):
                if ch == letter:
                    self.display[i] = letter
            return True
        else:
            self.lives -= 1
            return False

    def is_won(self):
        return "".join(self.display) == self.word

    def is_lost(self):
        return self.lives <= 0

    def get_display(self):
        return " ".join(self.display)
