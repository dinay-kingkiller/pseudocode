"""
A Wordle Solver v3

v1: tested each letter and position individually
v2: tested each letter and the pattern individually
v3: will check each word and generate the pattern difference
"""

import itertools

from collections import defaultdict
from string import ascii_lowercase as alphabet


class Solver:
    def __init__(self, targets, guesses, word_length=5, difficulty="disjoint"):
        """
        targets: list of possible target words
        guesses: list of possible guess words
        word_length: length of words in targets and guesses (default = 5)
        difficulty: how strict do guesses need to be
            disjoint = eliminates any guess with letters that have already been used.
            normal = guesses must be valid dictionary words.
            hard = exact letters must stay fixed. elsewhere letters must be reused.
            ultra = hard difficulty except elsewhere letters must be moved and absent letters cannot be used.
        """
        # Filter guesses by word_length.
        self.word_length = word_length
        self.targets = [word for word in targets if len(word) == word_length]
        self.guesses = [word for word in guesses if len(word) == word_length]

    def __next__(self):
        """
        returns the guess that has the most in common with the list of targets
        """
        # If no possible guesses, stop iterating.
        if not self.guesses:
            raise StopIteration

        # Calculate pattern frequency.
        frequency = dict()
        for guess in self.guesses:
            frequency[guess] = defaultdict(int())
            for goal in self.targets:
                pattern = self.compare_words(guess, goal)
                frequency[guess][pattern] += 1

        # Find the best guess.
        max_score = 0
        for guess in self.guesses:
            pattern_scores = self.frequency[guess].values()
            score = sum(
                [x*y for x, y in itertools.product(pattern_scores, pattern_scores)])
            score -= sum([x*x for x in pattern_scores])
            if score > max_score:
                max_score = score
                best_guess = guess
        return best_guess

    def compare_words(self, guess, target):
        """
        Compares a guess to a target word and returns information like Wordle.
        returns a pattern string:
            "e", exact: the guess and target letter match at that place
            "l", elsewhere: the guess letter is in the target, but not at that place
                It only sets this if the information from the target letter is not already used.
            "a", absent: any guess letters that remain
            "u", unknown: not yet checked. used in this function only
        """
        # Setup initial pattern to "u"nkown.
        pattern = ["u" for g in guess]

        # Check for "e"xact matches.
        for index, letter in enumerate(guess):
            if letter == target[index]:
                pattern[index] = "e"
                target[index] = None

        # Check for e"l"sewhere matches.
        for guess_index, guess_letter in enumerate(guess):
            if pattern[guess_index] != "u":
                # Skip already known parts of the pattern.
                continue
            for target_index, target_letter in enumerate(target):
                if guess_letter == target_letter:
                    pattern[guess_index] = "l"
                    # break to eliminate only the first target_letter
                    target[target_index] = None
                    break

        # Convert remaining "u"nknown to "a"bsent.
        for index, letter in enumerate(pattern):
            if letter == "u":
                pattern[index] = "a"

        return "".join(pattern)

    def update_disjoint(self, clues):
        """
        update_disjoint removes every word in guesses that has a letter in clues.
        """
        self.guesses = [word for word in self.guesses if all(
            letter not in clue for letter in word)]

    def update(self, clue):
        """
        Update targets and guesses based on the given clue.
        clue is an iterable of tuples: (letter, state)
        State can either be "exact", "elsewhere", or "absent".
        """
        for letter, state in clue:
            if state == "exact":

        for word in self.targets:
            self.validate_possible(
                word, exact_clue, elsewhere_clue, absent_clue)
        for word in self.guesses:
            if self.difficulty == "normal":
                break
            elif self.difficulty == "hard":
                self.validate_hard(
                    word, exact_clue, elsewhere_clue, absent_clue)
            elif self.difficulty == "ultra":
                self.validate_ultra(
                    word, exact_clue, elsewhere_clue, absent_clue)
            else:
                raise ValueError
        self.update_frequency()

    def validate_disjoint(self, used):
        """
        removes every word in guesses that has a letter in used.
        """
        for word in self.guesses:
            for letter in used:
                if letter in word:
                    self.guesses.remove(word)
                    break

    def validate_possible(self, word, exact_clue, elsewhere_clue, absent_clue):
        for position, letter in exact_clue:
            if word[position] != letter:
                self.possible_words.remove(word)
                return
        for position, letter in elsewhere_clue:
            if word[position] == letter:
                self.possible_words.remove(word)
                return
            elif letter not in word:
                self.possible_words.remove(word)
                return
            else:
                pass
        for letter in absent_clue:
            if letter in word:
                self.guess_words.remove(word)
                return

    def validate_normal(self, word, exact_clue, elsewhere_clue, absent_clue):
        pass

    def validate_hard(self, word, exact_clue, elsewhere_clue, absent_clue):
        present = set(i for _, i in elsewhere_clue)
        for letter in present:
            if letter not in word:
                self.guess_words.remove(word)
                return
        for position, letter in exact_clue:
            if word[position] != letter:
                self.guess_words.remove(word)
                return

    def validate_ultra(self, word, exact_clue, elsewhere_clue, absent_clue):
        for position, letter in exact_clue:
            if word[position] != letter:
                self.guess_words.remove(word)
                return
        for position, letter in elsewhere_clue:
            if word[position] == letter:
                self.guess_words.remove(word)
                return
            elif letter not in word:
                self.guess_words.remove(word)
                return
            else:
                pass
        for letter in absent_clue:
            if letter in word:
                self.guess_words.remove(word)
                return
