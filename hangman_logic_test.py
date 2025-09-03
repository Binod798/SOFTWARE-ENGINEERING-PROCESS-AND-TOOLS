"""
This file contains simplified Hangman game logic which is compatible with GUI and tests.
"""

import random
from enum import Enum

# --- Technology-themed words and phrases ---
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