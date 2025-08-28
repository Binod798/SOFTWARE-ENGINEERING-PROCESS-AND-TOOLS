import tkinter as tk
import random

# Technology-related words & phrases
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

HANGMAN_PICS = [
    "",
    " O ",
    " O \n | ",
    " O \n/| ",
    " O \n/|\\",
    " O \n/|\\\n/  ",
    " O \n/|\\\n/ \\"
]


class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")
        self.lives = 6
        self.time_limit = 15
        self.word = ""
        self.display = []
        self.mode = "basic"
        self.timer_id = None
        self.time_left = self.time_limit

        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack()

        self.show_start_screen()

    def show_start_screen(self):
        """Initial screen to choose game level"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        tk.Label(self.main_frame, text="🎮 Hangman Game", font=("Arial", 22, "bold")).pack(pady=20)
        tk.Label(self.main_frame, text="Choose Level:", font=("Arial", 14)).pack(pady=10)

        tk.Button(self.main_frame, text="Basic (Word)", font=("Arial", 14),
                  command=lambda: self.start_game("basic")).pack(pady=5)
        tk.Button(self.main_frame, text="Intermediate (Phrase)", font=("Arial", 14),
                  command=lambda: self.start_game("intermediate")).pack(pady=5)

    def start_game(self, mode):
        """Start the game after selecting level"""
        self.mode = mode
        self.lives = 6
        self.time_left = self.time_limit

        if mode == "basic":
            self.word = random.choice(WORDS).lower()
        else:
            self.word = random.choice(PHRASES).lower()

        self.display = ["_" if c != " " else " " for c in self.word]

        for widget in self.main_frame.winfo_children():
            widget.destroy()

        # Hangman drawing
        self.hangman_label = tk.Label(self.main_frame, text="", font=("Courier", 18), fg="red")
        self.hangman_label.pack()

        # Word display
        self.word_label = tk.Label(self.main_frame, text=" ".join(self.display), font=("Arial", 20))
        self.word_label.pack(pady=10)

        # Lives
        self.lives_label = tk.Label(self.main_frame, text=f"Lives: {self.lives}", font=("Arial", 14))
        self.lives_label.pack()

        # Timer
        self.timer_label = tk.Label(self.main_frame, text=f"Time left: {self.time_left}s", font=("Arial", 14), fg="blue")
        self.timer_label.pack()

        # Entry for guesses
        self.entry = tk.Entry(self.main_frame, font=("Arial", 14))
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.make_guess)

        self.message_label = tk.Label(self.main_frame, text="", font=("Arial", 12), fg="green")
        self.message_label.pack()

        # Start timer
        self.update_timer()

    def update_timer(self):
        """Countdown timer per guess"""
        if self.time_left > 0:
            self.timer_label.config(text=f"Time left: {self.time_left}s")
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.lives -= 1
            self.update_visuals()
            self.message_label.config(text="⏰ Time's up! You lost a life.", fg="red")
            self.reset_turn()

    def reset_turn(self):
        """Reset for next guess"""
        self.time_left = self.time_limit
        self.update_timer()

    def make_guess(self, event=None):
        guess = self.entry.get().lower().strip()
        self.entry.delete(0, tk.END)

        if not guess or len(guess) != 1 or not guess.isalpha():
            self.message_label.config(text="❌ Enter a single letter.", fg="red")
            return

        # Stop timer for this guess
        if self.timer_id:
            self.root.after_cancel(self.timer_id)

        if guess in self.word:
            for i, ch in enumerate(self.word):
                if ch == guess:
                    self.display[i] = guess
            self.message_label.config(text=f"✅ Good guess! '{guess}' is in the word/phrase.", fg="green")
        else:
            self.lives -= 1
            self.message_label.config(text=f"❌ Wrong guess! '{guess}' is not in the word/phrase.", fg="red")

        self.update_visuals()

        if "_" not in self.display:
            self.end_game(True)
        elif self.lives <= 0:
            self.end_game(False)
        else:
            self.reset_turn()

    def update_visuals(self):
        """Update word, lives, hangman drawing"""
        self.word_label.config(text=" ".join(self.display))
        self.lives_label.config(text=f"Lives: {self.lives}")
        self.hangman_label.config(text=HANGMAN_PICS[6 - self.lives])

    def end_game(self, won):
        """Game over screen"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        if won:
            tk.Label(self.main_frame, text="🎉 You Won!", font=("Arial", 22, "bold"), fg="green").pack(pady=20)
        else:
            tk.Label(self.main_frame, text="💀 Game Over!", font=("Arial", 22, "bold"), fg="red").pack(pady=20)

        tk.Label(self.main_frame, text=f"The correct word/phrase was: {self.word}", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.main_frame, text="Play Again", font=("Arial", 14), command=self.show_start_screen).pack(pady=10)
        tk.Button(self.main_frame, text="Quit", font=("Arial", 14), command=self.root.quit).pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Hangman Game")

    # Set window size and center it
    window_width = 800
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_pos = int((screen_width / 2) - (window_width / 2))
    y_pos = int((screen_height / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{x_pos}+{y_pos}")

    HangmanGame(root)
    root.mainloop()
