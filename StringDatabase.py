import random


class StringDatabase:
    """Loads the word file and picks random words."""

    def __init__(self, filename="four_letters.txt"):
        with open(filename) as f:
            self.words = f.read().split()

    def random_word(self):
        return random.choice(self.words).lower()
