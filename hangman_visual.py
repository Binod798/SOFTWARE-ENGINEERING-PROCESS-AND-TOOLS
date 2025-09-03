"""
hangman_visual.py

Tkinter GUI is used for the Hangman game.

Requirements satisfied:
- Level selection (Basic/Intermediate) inside the game visual.
- 15-second visible timer per guess; if time runs out, a life is deducted.
- Lives deducted on wrong guess; all positions revealed on correct guess.
- Effective hanging animation is done as lives are lost.
- The game continues until user quits, runs out of lives, or guesses correctly.
- Technology-themed words/phrases via hangman_core_logic.py.

Run:
    python hangmang_logic_test.py to run the tests and see detailed output.
    python hangman_visual.py to run the interface and play the game.
"""

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox
from typing import Optional

from hangman_core_logic import HangmanGame, Level

WINDOW_W, WINDOW_H = 800, 600
GUESS_SECONDS = 15

class HangmanApp(tk.Tk):
    #Tkinter application for Hangman game interface
    def __init__(self) -> None:
        super().__init__()
        self.title("Hangman — Software Engineering Process & Tools")
        self.geometry(f"{WINDOW_W}x{WINDOW_H}")
        self.resizable(False, False)

        # Game state
        self.game: HangmanGame = HangmanGame(level=Level.BASIC, max_attempts=6)
        self.timer_seconds: int = GUESS_SECONDS
        self.timer_job: Optional[str] = None  # after() id

        # Layout of the game
        self._build_top_bar()
        self._build_main_area()
        self._bind_events()

        self._refresh_all()

    # Construct the top bar with level selection and new game button.
    def _build_top_bar(self) -> None:
        top = tk.Frame(self, pady=8)
        top.pack(side=tk.TOP, fill=tk.X)

        # Level selection of radio buttons
        self.level_var = tk.StringVar(value=self.game.level.value)
        tk.Label(top, text="Level:").pack(side=tk.LEFT, padx=(10, 4))

        rb_basic = tk.Radiobutton(
            top, text="Basic (Word)", variable=self.level_var, value=Level.BASIC.value,
            command=self._on_level_change
        )
        rb_inter = tk.Radiobutton(
            top, text="Intermediate (Phrase)", variable=self.level_var, value=Level.INTERMEDIATE.value,
            command=self._on_level_change
        )
        rb_basic.pack(side=tk.LEFT)
        rb_inter.pack(side=tk.LEFT)

        # New Game button of the game
        tk.Button(top, text="New Game", command=self._new_game).pack(side=tk.LEFT, padx=10)

        # Spacer
        tk.Label(top, text=" " * 5).pack(side=tk.LEFT)