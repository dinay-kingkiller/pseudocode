"""
A Wordle Solver

This algorithm uses the list of targets and a dictionary to find the optimal next guess. The next best guess is determined by the most words from the target list it removes.

Scoring:
Take for an example, the word "erase"

For each letter in "erase" a pattern is picked out:
e: [T F F F T]
r: [F T F F F]
a: [F F T F F]
s: [F F F T F]

The sum of the letter scores equals the word score. For 'e' in "erase" for example:
guess pattern = [T F F F T]

This is compared to the frequency of each pattern of 'e' in the targets.  The only values you can gain data (for that letter) on are spaces where that letter exist. So for "erase" the middle three letters can be ignored for patterns of 'e'. Patterns that contain 'e' at the same spot would be labeled "exact". [T F F F F] and [T F F T F] would be "exact" at the first spot. "elsewhere" is a bit more complicated. So for each pattern, count the number of instances of the letter minus the "exact" positions. Then, starting at the leftmost non-"exact" instance, use up this count, filling spots with "elsewhere"s. Finally any remaining instances in the pattern should be filled with "absent"
[T F F F T]:
[F T F F T] -> [L U U U E]
[F T T F F] -> [L U U U L]
[F T F F F] -> [L U U U A]
[F F F F T] -> [A U U U E]

["exact", "unknown", "unknown", "unknown", "exact"]
If the first letter is 'e', and there is at least one more 'e'
["exact", "unknown", "unknown", "unknown", "elsewhere"]
["exact", "unknown", "unknown", "unknown", "absent"]
["elsewhere", "unknown", "unknown", "unknown", "exact"]
["elsewhere", "unknown", "unknown", "unknown", "elsewhere"]
["elsewhere", "unknown", "unknown", "unknown", "absent"]
["absent", "unknown", "unknown", "unknown", "exact"]
["absent", "unknown", "unknown", "unknown", "elsewhere"]
["absent", "unknown", "unknown", "unknown", "absent"]
"""


from string import ascii_lowercase as alphabet
import json
rarest_word = "murky"


def json_reader(filename):
    with open("targets.json", 'r') as file:
        data = json.loads(file.read())
    return data


def initial_filter(word_list, word_length):
    word_list = filter(lambda x: len(
        x) == word_length and x != '*'*word_length, word_list)
    return word_list


class Solver:
    def __init__(self, target_list, dictionary, word_length=5, difficulty="disjoint"):
        self.targets = target_list
        self.dictionary = dictionary
        self.word_length = word_length

    def __next__(self):
        if not self.dictionary:
            raise StopIteration
        self.update_frequency()
        max_score = 0
        for guess in self.dictionary:
            score = self.score_word(guess)
            if score > max_score:
                max_score = score
                best_guess = guess
        return best_guess

    def update_frequency(self):
        self.frequency = {letter: {} for letter in alphabet}
        present = {letter: 0 for letter in alphabet}
        list_length = 0
        for word in self.targets:
            list_length += 1
            for index, letter in enumerate(word):
                assert index < word_length
                if letter not in word[index+1:]:
                    pattern = [letter == other_letter for other_letter in word]
                    key = self._letter_pattern2key(pattern)
                    present[letter] += 1
                    if key in self.frequency[letter]:
                        self.frequency[letter][key] += 1
                    else:
                        self.frequency[letter][key] = 1
        absent = {letter: list_length-present[letter] for letter in alphabet}
        for letter in alphabet:
            self.frequency[letter][0] = absent[letter]
        return self.frequency

    def score_word(self, word):
        score = 0
        for index, letter in enumerate(word):
            if letter not in word[index+1:]:
                letter_pattern = [let == letter for let in word]
                score += self.score_letter(letter, letter_pattern)
        return score

    def score_letter(self, letter, pattern):
        possibilities = {}
        for freq_key in self.frequency[letter]:
            freq_pattern = self._key2letter_pattern(freq_key)
            guess_pattern = self.compare_patterns(pattern, freq_pattern)
            guess_key = self._guess_pattern2key(guess_pattern)
            if guess_key in possibilities:
                possibilities[guess_key] += self.frequency[letter][freq_key]
            else:
                possibilities[guess_key] = self.frequency[letter][freq_key]
        return self._poss_prod(possibilities.values())

    def compare_patterns(self, target, guess):
        # TODO fix double elsewhere letters. fix'd??
        compared = ["unknown"] * self.word_length
        target = list(target)
        guess = list(guess)
        for index in range(self.word_length):
            if target[index] and guess[index]:
                compared[index] = "exact"
                target[index] = False
                guess[index] = False
        for target_index in range(self.word_length):
            if target[target_index]:
                for guess_index in range(self.word_length):
                    if guess[guess_index] and not target[guess_index]:
                        compared[target_index] = "elsewhere"
                        target[target_index] = False
                        guess[guess_index] = False
                        break
        for index in range(self.word_length):
            if target[index] and target[index] not in guess:
                compared[index] = "absent"
        return compared

    def _letter_pattern2key(self, pattern):
        return sum([value*2**index for index, value in enumerate(reversed(pattern))])

    def _guess_pattern2key(self, pattern):
        converter = {"unknown": 0, "absent": 1, "elsewhere": 2, "exact": 3}
        return sum([converter[value]*4**index for index, value in enumerate(pattern)])

    def _key2letter_pattern(self, key):
        index = 0
        pattern = [False]*self.word_length
        for i in range(self.word_length):
            pattern[i] = key % 2 == 1
            key = key//2
            index += 1
        return list(reversed(pattern))

    def _poss_prod(self, vector):
        total = 0
        for val1 in vector:
            for val2 in vector:
                if val1 != val2:
                    total += val1*val2
        return total

    def use_clues(self, exact_clue, elsewhere_clue, absent_clue):
        for word in self.valid_list:
            self.validate_possible(
                word, exact_clue, elsewhere_clue, absent_clue)
        for word in self.guess_words:
            if self.difficulty == 0:
                pass
            elif self.difficulty == 1:
                self.validate_hard(
                    word, exact_clue, elsewhere_clue, absent_clue)
            elif self.difficulty == 2:
                self.validate_ultra(
                    word, exact_clue, elsewhere_clue, absent_clue)
            else:
                raise ValueError
        self.update_frequency()

    def validate_disjoint(self, letters):
        for word in list(self.dictionary):
            for letter in letters:
                if letter in word:
                    self.dictionary.remove(word)
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


if __name__ == "__main__":
    word_length = 5
    targets = json_reader("targets.json")
    dictionary = json_reader("dictionary.json")
    targets = list(initial_filter(targets, word_length))
    dictionary = list(initial_filter(dictionary, word_length))
    solver = Solver(targets, dictionary, word_length)
    solver.update_frequency()
    freq = solver.frequency['e']
    lst = list(freq)
    lst.sort()
    for key in lst:
        pattern = solver._key2letter_pattern(key)
        # print(pattern,": ",freq[key])
    guesses = []
    guesses.append(next(solver))
    print(guesses)
    solver.validate_disjoint("".join(guesses))
    guesses.append(next(solver))
    print(guesses)
    solver.validate_disjoint("".join(guesses))
    guesses.append(next(solver))
    print(guesses)
    solver.validate_disjoint("".join(guesses))
    guesses.append(next(solver))
    print(guesses)
