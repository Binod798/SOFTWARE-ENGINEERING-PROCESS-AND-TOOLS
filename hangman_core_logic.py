"""
This file contains simplified Hangman game logic which is compatible with GUI and tests.
"""

import random
from enum import Enum


TECH_WORDS = [
    "python", "database", "compiler", "encryption",
    "firewall", "variable", "function", "interface",
    "protocol", "container", "debugger", "bandwidth",
]

TECH_PHRASES = [
    "machine learning", "cloud computing",
    "software engineering", "unit testing",
    "version control", "data structures",
]
   
class Level(Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"


class HangmanGame:
    """Simple Hangman game logic."""

    def __init__(self, level=Level.BASIC, max_attempts=6, rng_seed=None):
        self.level = level
        self.max_attempts = max_attempts
        self.rng = random.Random(rng_seed) 
        self.answer = ""
        self.masked = []
        self.attempts_left = max_attempts
        self.guessed_letters = set()
        self.choose_new_answer(level)

    def choose_new_answer(self, level=None):
        """Pick a random word or phrase depending on level."""
        if level:
            self.level = level
        if self.level == Level.BASIC:
            self.answer = self.rng.choice(TECH_WORDS)
        else:
            self.answer = self.rng.choice(TECH_PHRASES)

        self.answer = self.answer.lower()
        self.attempts_left = self.max_attempts
        self.guessed_letters = set()
        self.masked = self._make_masked()

    def _make_masked(self):
        """Return masked list with underscores for hidden letters."""
        return [ch if (not ch.isalpha()) else "_" for ch in self.answer]

    def mask_answer(self, answer, guessed):
        """
        Public method for tests:
        Returns masked version of `answer`, revealing guessed letters.
        """
        return [ch if (not ch.isalpha()) or (ch in guessed) else "_" for ch in answer]

    def guess_letter(self, letter):
        """
        Process a guess:
        - Returns (correct, positions)
        - Deducts life if wrong.
        """
        if not (len(letter) == 1 and letter.isalpha()):
            raise ValueError("Please guess a single alphabetic letter.")

        letter = letter.lower()

        if letter in self.guessed_letters:
            return False, []  # no penalty

        self.guessed_letters.add(letter)
        positions = [i for i, ch in enumerate(self.answer) if ch == letter]

        if positions:
            for i in positions:
                self.masked[i] = letter
            return True, positions
        else:
            self.attempts_left -= 1
            return False, []

    def is_won(self):
        # Check if all letters are revealed
        return all(
            (not ch.isalpha()) or (self.masked[i] == ch)
            for i, ch in enumerate(self.answer)
        )

    def is_lost(self):
        # Check if lives are zero
        return self.attempts_left <= 0

    def get_display_word(self):
        # Return masked word as string
        return " ".join(self.masked)

    def reveal_all(self):
        # Show the full answer if the game is ended
        self.masked = list(self.answer)


__all__ = ["HangmanGame", "Level", "TECH_WORDS", "TECH_PHRASES"]