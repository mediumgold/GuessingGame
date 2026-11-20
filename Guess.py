import os
from Game import Game
from StringDatabase import StringDatabase

FREQUENCIES = {
    "a": 8.17, "b": 1.49, "c": 2.78, "d": 4.25, "e": 12.70, "f": 2.23,
    "g": 2.02, "h": 6.09, "i": 6.97, "j": 0.15, "k": 0.77, "l": 4.03,
    "m": 2.41, "n": 6.75, "o": 7.51, "p": 1.93, "q": 0.10, "r": 5.99,
    "s": 6.33, "t": 9.06, "u": 2.76, "v": 0.98, "w": 2.36, "x": 0.15,
    "y": 1.97, "z": 0.07,
}


class Guess:
    """Core game logic: menu, user input and scoring."""

    def __init__(self, test_mode):
        self.test_mode = test_mode
        self.db = StringDatabase()
        self.games = []
        self.new_game()

    def new_game(self):
        self.game = Game(self.db.random_word())
        self.revealed = ["-"] * len(self.game.word)
        self.letters = []
        self.requests = 0

    def start(self):
        while True:
            self.show_menu()
            option = input("Enter Option: ").strip().lower()
            while option not in ("g", "t", "l", "q"):
                option = input("\nInvalid option. Please re-enter: ").strip().lower()

            if option == "q":
                self.report()
                return
            if option == "g":
                finished = self.guess_word()
            elif option == "t":
                finished = self.give_up()
            else:
                finished = self.guess_letter()

            input("\nPress any key to continue... ")
            if finished:
                self.games.append(self.game)
                self.new_game()

    def show_menu(self):
        self.clear()
        print("++\n++ The great guessing game\n++\n")
        if self.test_mode:
            print(f"Current Word:  {self.game.word}")
        print(f"Current Guess:  {''.join(self.revealed)}")
        print(f"Letters guessed: {' '.join(self.letters)}")
        print("\ng = guess, t = tell me, l for a letter, and q to quit\n")

    def guess_word(self):
        attempt = input("\nMake your guess: ").strip().lower()
        if attempt == self.game.word:
            penalty = 1 - 0.1 * self.game.bad_guesses
            self.game.status = "Success"
            self.game.score = self.remaining_points() / max(self.requests, 1) * penalty
            self.feedback("You're right, Einstein!")
            return True
        self.game.bad_guesses += 1
        self.feedback("Try again, Loser!")
        return False

    def give_up(self):
        self.game.status = "Gave up"
        self.game.score = -self.remaining_points()
        self.feedback(f"You really should have guessed this...'{self.game.word}'")
        return True

    def guess_letter(self):
        letter = input("\nEnter a letter: ").strip().lower()
        while letter not in FREQUENCIES:
            letter = input("Please enter a single letter: ").strip().lower()

        if letter in self.letters:
            self.feedback(f"You already tried '{letter}'")
            return False

        self.letters.append(letter)
        self.requests += 1
        found = self.game.word.count(letter)
        if found:
            self.revealed = [c if c == letter else r for c, r in zip(self.game.word, self.revealed)]
            self.feedback(f"Woo hoo, you found {found} letters")
        else:
            self.game.missed_letters += 1
            self.feedback("Not a single match, genius")
        return False

    def remaining_points(self):
        return sum(FREQUENCIES[c] for c, r in zip(self.game.word, self.revealed) if r == "-")

    def report(self):
        self.clear()
        print("++\n++ Game Report\n++\n")
        row = "{:<8}{:<8}{:<10}{:<14}{:<17}{}"
        print(row.format("Game", "Word", "Status", "Bad Guesses", "Missed Letters", "Score"))
        print(row.format("----", "----", "------", "-----------", "--------------", "-----"))
        for i, g in enumerate(self.games, 1):
            print(row.format(i, g.word, g.status, g.bad_guesses, g.missed_letters, f"{g.score:.2f}"))
        print(f"\nFinal Score: {sum(g.score for g in self.games):.2f}")

    @staticmethod
    def feedback(message):
        print(f"\n@@\n@@ FEEDBACK: {message}\n@@")

    @staticmethod
    def clear():
        os.system("cls" if os.name == "nt" else "clear")
