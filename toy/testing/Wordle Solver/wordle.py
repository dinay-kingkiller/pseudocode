"""
A Wordle Solver v3

v1: tested each letter and position individually
v2: tested each letter and the pattern individually
v3: will check each word and generate the pattern difference
"""


from string import ascii_lowercase as alphabet
import json
rarest_word = "murky"
def json_reader(filename):
    with open("targets.json",'r') as file:
        data=json.loads(file.read())
    return data
def initial_filter(word_list, word_length):
    word_list = filter(lambda x: len(x)==word_length and x!='*'*word_length, word_list)
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
    def score_word(self, guess):
        return self._poss_prod(self.frequency[guess].values())
    def update_frequency(self):
        self.frequency = {}
        for guess in self.dictionary:
            self.frequency[guess] = {}
            for goal in self.targets:
                pattern = self.compare_words(guess, goal)
                key = self._guess_pattern2key(pattern)
                if key in self.frequency[guess]:
                    self.frequency[guess][key] += 1
                else:
                    self.frequency[guess][key] = 1
        return self.frequency
    def compare_words(self, guess, target):
        pattern = ["unknown"]*self.word_length
        guess = list(guess)
        target = list(target)
        for guess_index in range(self.word_length):
            if guess[guess_index] == target[guess_index]:
                pattern[guess_index] = "exact"
                target[guess_index] = None
            elif guess[guess_index] in target:
                for target_index in range(self.word_length):
                    if guess[guess_index] == target[target_index]:
                        pattern[guess_index] = "elsewhere"
                        target[target_index] = None
                        break
            else:
                pattern[guess_index] = "absent"
        return pattern
    def _letter_pattern2key(self, pattern):
        return sum([value*2**index for index, value in enumerate(reversed(pattern))])
    def _guess_pattern2key(self, pattern):
        converter = {"unknown":0, "absent":1, "elsewhere":2, "exact":3}
        return sum([converter[value]*4**index for index, value in enumerate(pattern)])
    def _key2letter_pattern(self, key):
        index=0
        pattern=[False]*self.word_length
        for i in range(self.word_length):
            pattern[i]=key%2==1
            key=key//2
            index+=1
        return list(reversed(pattern))
    def _poss_prod(self, vector):
        total = 0
        for val1 in vector:
            for val2 in vector:
                if val1!=val2:
                    total+=val1*val2
        return total
    def use_clues(self, exact_clue, elsewhere_clue, absent_clue):
        for word in self.valid_list:
            self.validate_possible(word, exact_clue, elsewhere_clue, absent_clue)
        for word in self.guess_words:
            if self.difficulty==0:
                pass
            elif self.difficulty==1:
                self.validate_hard(word, exact_clue, elsewhere_clue, absent_clue)
            elif self.difficulty==2:
                self.validate_ultra(word, exact_clue, elsewhere_clue, absent_clue)
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
            if word[position]!=letter:
                self.possible_words.remove(word)
                return
        for position, letter in elsewhere_clue:
            if word[position]==letter:
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
            if word[position]!=letter:
                self.guess_words.remove(word)
                return
    def validate_ultra(self, word, exact_clue, elsewhere_clue, absent_clue):
        for position, letter in exact_clue:
            if word[position]!=letter:
                self.guess_words.remove(word)
                return
        for position, letter in elsewhere_clue:
            if word[position]==letter:
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
def fun1(targets, dictionary):
    target_frequency = {}
    present = {}
    list_length = 0
    for word in targets:
        list_length += 1
        for letter in set(word):
            if letter not in target_frequency:
                target_frequency[letter] = {}
            if letter not in present:
                present[letter] = 0
            present[letter] += 1
            pattern = [letter==other_letter for other_letter in word]
            key = get_key2(pattern)
            if key in target_frequency:
                target_frequency[letter][key] += 1
            else:
                target_frequency[letter][key] = 1
        for letter in target_frequency:
            assert list_length > present[letter]
            target_frequency[letter][0] = list_length - present[letter]
    best_guess = None
    max_score = 0
    for word in dictionary:
        word_length = len(word)
        score = 1
        for letter in set(word):
            compared_frequency = {}
            for pattern in target_frequency[letter]:
                assert len(pattern) == word_length
                guess_pattern = [letter==other_letter for other_letter in word]
                target_pattern = list(pattern)
                compared_pattern = ["unknown"] * word_length
                for index in range(word_length):
                    if guess_pattern[index] and target_pattern[index]:
                        compared_pattern[index] = "exact"
                        guess_pattern[index] = False
                        target_pattern[index] = False
                        continue
                for guess_index in range(word_length):
                    if not guess_pattern[guess_index] or guess_pattern[guess_index] not in target_pattern:
                        continue
                    for target_index in range(word_length):
                        if guess_pattern[guess_index] and target_pattern[target_index]:
                            compared_pattern[guess_index] = "elsewhere"
                            guess_pattern[guess_index] = False
                            target_pattern[target_index] = False
                for index in range(word_length):
                    if guess[index] and guess[index] not in target:
                        compared_pattern[index] = "absent"
                key = get_key4(compared_pattern)
                if key in compared_frequency:
                    compared_frequency[key] += 1
                else:
                    compared_frequency[key] = 1
            score += cross_product(compared_frequency.values())
        if score > max_score:
            best_guess = word
            max_score = score
    return best_guess
def fun2(targets, dictionary):
    best_guess = None
    max_score = 0
    for word in dictionary:
        word_length = len(word)
        score = 1
        for target in targets:
            assert len(target) == word_length
            guess = list(word)
            goal = list(target)
            compared_pattern = ["unknown"] * word_length
            for index in range(word_length):
                if guess[index] == goal[index]:
                    compared_pattern[index] = "exact"
                    guess[index] = None
                    goal[index] = None





if __name__=="__main__":
    word_length = 5
    targets = json_reader("targets.json")
    dictionary = json_reader("dictionary.json")
    targets = list(initial_filter(targets, word_length))
    dictionary = list(initial_filter(dictionary, word_length))
    solver = Solver(targets,dictionary,word_length)
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
    