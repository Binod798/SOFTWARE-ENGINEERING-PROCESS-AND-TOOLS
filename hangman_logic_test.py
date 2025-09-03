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
    
    def test_choose_new_answer_intermediate(self) -> None:
        self.game.choose_new_answer(Level.INTERMEDIATE)
        print(f"[Test] New INTERMEDIATE level phrase selected: '{self.game.answer}'")
        self.assertIn(self.game.answer, TECH_PHRASES)
        print("✅ The phrase is valid and comes from the INTERMEDIATE dictionary.")

    def test_correct_guess_reveals_all_positions(self) -> None:
        self.game.answer = "protocol"
        self.game.masked = self.game.mask_answer(self.game.answer, set())
        ok, positions = self.game.guess_letter('o')
        print(f"[Test] Guessing the letter 'o' in '{self.game.answer}'...")
        print(f"   🎯 Correct! The letter 'o' appears {len(positions)} time(s) at positions {positions}.")
        self.assertTrue(ok)
        self.assertEqual(positions, [2, 4, 6])
        print(f"   ✅ Current word display: {self.game.get_display_word()}")
        
    def test_wrong_guess_deducts_life(self) -> None:
        self.game.answer = "python"
        self.game.masked = self.game.mask_answer(self.game.answer, set())
        lives_before = self.game.attempts_left
        ok, positions = self.game.guess_letter('e')
        print(f"[Test] Guessing the letter 'e' in '{self.game.answer}'...")
        print(f"   ❌ Wrong guess! Life deducted. Lives remaining: {self.game.attempts_left}")
        self.assertFalse(ok)
        self.assertEqual(positions, [])
        self.assertEqual(self.game.attempts_left, lives_before - 1)

    def test_repeated_guess_no_penalty(self) -> None:
        self.game.answer = "debugger"
        self.game.masked = self.game.mask_answer(self.game.answer, set())
        ok1, _ = self.game.guess_letter('g')
        lives_after_first = self.game.attempts_left
        ok2, _ = self.game.guess_letter('g')
        print(f"[Test] Guessing the letter 'g' twice in '{self.game.answer}'...")
        print(f"   ✅ First guess successful. Lives remaining: {lives_after_first}")
        print(f"   🔄 Second guess ignored. Lives still: {self.game.attempts_left}")
        self.assertFalse(ok2)
        self.assertEqual(self.game.attempts_left, lives_after_first)

   

if __name__ == "__main__":
    unittest.main(verbosity=2)
