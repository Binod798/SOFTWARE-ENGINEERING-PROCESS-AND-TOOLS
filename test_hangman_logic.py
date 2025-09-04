import unittest
from hangman_logic import HangmanLogic

class TestHangmanLogic(unittest.TestCase):

    def test_word_generation_basic(self):
        game = HangmanLogic(mode="basic")
        print(f"[DEBUG] Generated word (basic): {game.word}")
        self.assertIn(game.word, [
            "python", "java", "linux", "docker", "git",
            "cloud", "api", "debug", "server", "binary"
        ])

    def test_word_generation_intermediate(self):
        game = HangmanLogic(mode="intermediate")
        print(f"[DEBUG] Generated phrase (intermediate): {game.word}")
        self.assertIn(game.word, [
            "machine learning", "artificial intelligence", "software engineering",
            "data science", "open source", "computer network",
            "object oriented programming", "operating system",
            "cloud computing", "version control"
        ])

    def test_invalid_mode_raises_error(self):
        print("[DEBUG] Testing invalid mode...")
        with self.assertRaises(ValueError):
            HangmanLogic(mode="invalid")

    def test_correct_guess_reveals_letter(self):
        game = HangmanLogic()
        game.word = "python"
        game.display = ["_", "_", "_", "_", "_", "_"]
        result = game.guess("p")
        print(f"[DEBUG] Guess 'p': result={result}, display={game.display}")
        self.assertTrue(result)
        self.assertEqual(game.display[0], "p")

    def test_wrong_guess_reduces_lives(self):
        game = HangmanLogic(lives=3)
        game.word = "java"
        game.display = ["_", "_", "_", "_"]
        result = game.guess("z")
        print(f"[DEBUG] Guess 'z': result={result}, lives={game.lives}")
        self.assertFalse(result)
        self.assertEqual(game.lives, 2)

    def test_guess_reveals_all_occurrences(self):
        game = HangmanLogic()
        game.word = "data"
        game.display = ["_", "_", "_", "_"]
        result = game.guess("a")
        print(f"[DEBUG] Guess 'a': display={game.display}")
        self.assertTrue(result)
        self.assertEqual(game.display, ["_", "a", "_", "a"])

    def test_win_condition(self):
        game = HangmanLogic()
        game.word = "ai"
        game.display = ["a", "i"]
        print(f"[DEBUG] Win condition: display={game.display}")
        self.assertTrue(game.is_won())

    def test_loss_condition(self):
        game = HangmanLogic(lives=0)
        print(f"[DEBUG] Loss condition: lives={game.lives}")
        self.assertTrue(game.is_lost())

    def test_display_format(self):
        game = HangmanLogic()
        game.word = "git"
        game.display = ["g", "_", "t"]
        display_text = game.get_display()
        print(f"[DEBUG] Display format: {display_text}")
        self.assertEqual(display_text, "g _ t")


if __name__ == "__main__":
    unittest.main()
