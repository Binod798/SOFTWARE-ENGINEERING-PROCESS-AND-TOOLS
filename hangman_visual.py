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
        
    def _bind_events(self) -> None:
        self.bind("<Return>", lambda _e: self._on_guess())

    #Refresh and update UI elements 
    def _on_level_change(self) -> None:
        value = self.level_var.get()
        level = Level.BASIC if value == Level.BASIC.value else Level.INTERMEDIATE
        self.game.choose_new_answer(level)
        self.entry.config(state=tk.NORMAL)
        self._reset_timer()
        self._refresh_all()

    def _new_game(self) -> None:
        # Start a new game at current level
        value = self.level_var.get()
        level = Level.BASIC if value == Level.BASIC.value else Level.INTERMEDIATE
        self.game.choose_new_answer(level)
        self.entry.config(state=tk.NORMAL)
        self.message_label.config(text="")
        self._reset_timer()
        self._refresh_all()

    def _on_guess(self) -> None:
        text = self.entry.get().strip()
        self.entry.delete(0, tk.END)
        if not text:
            return
        if len(text) != 1 or not text.isalpha():
            messagebox.showinfo("Invalid", "Please enter a single alphabetic letter (a-z).")
            return

        try:
            correct, positions = self.game.guess_letter(text)
        except ValueError as e:
            messagebox.showinfo("Invalid", str(e))
            return

        if correct:
            self.message_label.config(
                text=f"Nice! The letter '{text.lower()}' is in the answer at {len(positions)} position(s).",
                fg="green"
            )
        else:
            self.message_label.config(text=f"Oops! The letter '{text.lower()}' is not in the answer.", fg="red")
            self._draw_hangman_stage()

        self._refresh_labels()
        self._check_end_state()
        self._reset_timer()

    # Redraw hangman based on lives left
    def _reset_timer(self) -> None:
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None
        self.timer_seconds = GUESS_SECONDS
        self.timer_label.config(text=f"Time left: {self.timer_seconds}s")
        self.timer_job = self.after(1000, self._tick)

    def _tick(self) -> None:
        self.timer_seconds -= 1
        self.timer_label.config(text=f"Time left: {self.timer_seconds}s")
        if self.game.is_won() or self.game.is_lost():
            return
        if self.timer_seconds <= 0:
            self.game.attempts_left -= 1
            self.message_label.config(text="Time's up! Life deducted.", fg="orange")
            self._draw_hangman_stage()
            self._refresh_labels()
            self._check_end_state()
            self._reset_timer()
            return
        self.timer_job = self.after(1000, self._tick)
        
    # Refresh all UI elements
    def _refresh_all(self) -> None:
        self._clear_canvas()
        self._draw_gallows()
        self._draw_hangman_stage()
        self._refresh_labels()

    def _refresh_labels(self) -> None:
        self.word_label.config(text=self.game.get_display_word())
        self.lives_label.config(text=f"Lives: {self.game.attempts_left}")
        guessed = ", ".join(sorted(self.game.guessed_letters)) if self.game.guessed_letters else "—"
        self.guessed_label.config(text=f"Guessed: {guessed}")

    def _check_end_state(self) -> None:
        if self.game.is_won():
            self.message_label.config(text="🎉 You guessed it! Press 'New Game' to play again.", fg="green")
            self._stop_timer()
            self.game.reveal_all()
            self._refresh_labels()
            self.entry.config(state=tk.DISABLED)
        elif self.game.is_lost():
            self.message_label.config(text=f"💀 Game over! The answer was: '{self.game.answer}'.", fg="red")
            self._stop_timer()
            self.game.reveal_all()
            self._refresh_labels()
            self.entry.config(state=tk.DISABLED)
        else:
            self.entry.config(state=tk.NORMAL)

    def _stop_timer(self) -> None:
        if self.timer_job is not None:
            self.after_cancel(self.timer_job)
            self.timer_job = None

  

    def _clear_canvas(self) -> None:
        self.canvas.delete("all")

    def _draw_gallows(self) -> None:
        self.canvas.create_line(50, 380, 350, 380, width=3)   # base
        self.canvas.create_line(100, 380, 100, 80, width=3)   # vertical
        self.canvas.create_line(100, 80, 260, 80, width=3)    # top
        self.canvas.create_line(260, 80, 260, 130, width=3)   # rope

    def _draw_hangman_stage(self) -> None:
        stage = self.game.max_attempts - self.game.attempts_left
        if stage >= 1:
            self.canvas.create_oval(230, 130, 290, 190, width=3)  # head
        if stage >= 2:
            self.canvas.create_line(260, 190, 260, 260, width=3)  # body
        if stage >= 3:
            self.canvas.create_line(260, 210, 230, 240, width=3)  # left arm
        if stage >= 4:
            self.canvas.create_line(260, 210, 290, 240, width=3)  # right arm
        if stage >= 5:
            self.canvas.create_line(260, 260, 235, 310, width=3)  # left leg
        if stage >= 6:
            self.canvas.create_line(260, 260, 285, 310, width=3)  # right leg
            
if __name__ == "__main__":
    app = HangmanApp()
    app.mainloop()