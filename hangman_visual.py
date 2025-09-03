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

        # Spacer between left and right
        tk.Label(top, text=" " * 5).pack(side=tk.LEFT)
        
         # Lives and timer display
        self.lives_label = tk.Label(top, text="Lives: 6", font=("Arial", 12, "bold"))
        self.lives_label.pack(side=tk.LEFT, padx=10)

        self.timer_label = tk.Label(top, text=f"Time left: {GUESS_SECONDS}s", font=("Arial", 12))
        self.timer_label.pack(side=tk.LEFT, padx=10)

        # Guessed letters display
        self.guessed_label = tk.Label(top, text="Guessed: —")
        self.guessed_label.pack(side=tk.RIGHT, padx=12)

    def _build_main_area(self) -> None:
        body = tk.Frame(self)
        body.pack(fill=tk.BOTH, expand=True)

        # Left: Canvas for hangman drawing
        self.canvas = tk.Canvas(body, width=400, height=420, bg="white")
        self.canvas.pack(side=tk.LEFT, padx=20, pady=10)

        # Right: Word display and controls
        right = tk.Frame(body)
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.word_label = tk.Label(right, text="_", font=("Consolas", 24))
        self.word_label.pack(pady=(20, 10))

        entry_row = tk.Frame(right)
        entry_row.pack(pady=5)
        tk.Label(entry_row, text="Your guess (a-z): ").pack(side=tk.LEFT)
        self.entry = tk.Entry(entry_row, width=5, font=("Consolas", 18))
        self.entry.pack(side=tk.LEFT)
        tk.Button(entry_row, text="Guess", command=self._on_guess).pack(side=tk.LEFT, padx=6)

        self.message_label = tk.Label(right, text="", fg="blue")
        self.message_label.pack(pady=10)

        # Footer with tips
        self.footer_label = tk.Label(
            right,
            text="Tip: press Enter to submit a guess • Repeated guesses are ignored without penalty.",
            fg="gray",
        )
        self.footer_label.pack(side=tk.BOTTOM, pady=10)