class Game:
    """Stores the results of one game for the final report."""

    def __init__(self, word):
        self.word = word
        self.status = ""
        self.bad_guesses = 0
        self.missed_letters = 0
        self.score = 0.0
