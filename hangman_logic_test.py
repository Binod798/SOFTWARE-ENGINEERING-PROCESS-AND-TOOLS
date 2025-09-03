import unittest
from hangman_core_logic import HangmanGame, Level, TECH_WORDS, TECH_PHRASES

class TestHangmanCoreLogic(unittest.TestCase):
    def setUp(self) -> None:
        # Seed for deterministic answer selection
        self.game = HangmanGame(level=Level.BASIC, max_attempts=6, rng_seed=42)
        print("\n[Setup] A new game has started with BASIC level!")

    def test_valid_dictionaries(self) -> None:
        print("[Test] Checking if word and phrase lists are ready...")
        self.assertGreater(len(TECH_WORDS), 0, "Oops! No words found in TECH_WORDS.")
        self.assertGreater(len(TECH_PHRASES), 0, "Oops! No phrases found in TECH_PHRASES.")
        print("✅ Word and phrase lists are ready to use!")

    def test_choose_new_answer_basic(self) -> None:
        self.game.choose_new_answer(Level.BASIC)
        print(f"[Test] New BASIC level word selected: '{self.game.answer}'")
        self.assertIn(self.game.answer, TECH_WORDS)
        print("✅ The word is valid and comes from the BASIC dictionary.")

   

if __name__ == "__main__":
    unittest.main(verbosity=2)
