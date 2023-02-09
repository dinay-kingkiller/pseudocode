
"""
How to score

The word that removes the most other words is the highest scorer.

R first letter has:
exact_freq/len(word_list) to be exact
elsewhere_freq/len(word_list) to be elsewhere
absent_freq/len(word_list) to be absent

if it is exact it will eliminate elsewhere_freq+absent_freq words
if it is elsewhere it will eliminate exact_freq+absent_freq words
if it is absent it will eliminate exact_freq+elsewhere_freq words

soooo

score = exact*(elsewhere+absent) + elsewhere*(exact+absent) + absent*(exact+elsewhere)...
=2*exact*elsewhere+2*exact*absent+2*elsewhere*absent...
=exact*elsewhere+exact*absent+elsewhere*absent

Take the word list:
["RAISE","RARLY","CARRY","COUNT"]
exact[R] = [2,0,2,1,0]
elsewhere[R]= [1,3,1,2,3]
absent[R]=1

exact[C] = [2,0,0,0,0]
elsewhere[C] = [0,2,2,2,2]
absent[C] = 2

First letter only score

score[RAISE]=2+1+2
score[RARLY]=2+1+2
score[COUNT]=2+2
score[XRXXX]=0

RAISE wins!!

BATCH
CATCH
HATCH
MATCH
exact[M] = [1,0,0,0,0]
elsewhere[M] = [0,1,1,1,1]
absent[M] = [3,0,0,0,0]
exact[H] = [1,0,0,0,1]
elsewhere[H] = [3,4,4,4,0]
absent[H] = 0

M = 1*0+0*0+1*0

v2

'A' first letter has:
exact_freq/len(word_list) to be exact
elsewhere_freq/len(word_list) to be elsewhere
absent_freq/len(word_list) to be absent

if it is exact it will eliminate elsewhere_freq+absent_freq words
if it is elsewhere it will eliminate exact_freq+absent_freq words
if it is absent it will eliminate exact_freq+elsewhere_freq words

soooo

score = exact*(elsewhere+absent) + elsewhere*(exact+absent) + absent*(exact+elsewhere)...
=2*exact*elsewhere+2*exact*absent+2*elsewhere*absent...
=exact*elsewhere+exact*absent+elsewhere*absent

New list: AAA, AAB, ABA, ABB, BAA, BAB, BBA, BBB
[A][A][_]
[A][A][_]
[A](A)[_]
[A]{A}[_]
(A)[A][_]
{A}[A][_]
(A){A}[_]
{A}{A}[_]


[A][A][_]
[A](A)[_]
[A]{A}[_]
(A)[A][_]
{A}[A][_]
(A){A}[_]
{A}{A}[_]

A*(B+C)+B*(A+C)+C*(A+B)
A*B+A*C+B*A+B*C+C*A+C*B
sum(sum(P_i * P_j for j~=i) for i)

okay so you have a dict
of dicts
dict['a'] gives you another dict

"""
from string import ascii_lowercase as alphabet
from itertools import product
import json
rarest_word = "murky"


def json_reader(filename):
    with open("targets.json", 'r') as file:
        data = json.loads(file.read())
    return data


class Solver:
    def __init__(self, possible_words, guess_words, word_length=5, difficulty=0):
        self.possible_words = possible_words
        self.guess_words = guess_words
        self.word_length = word_length
        self.difficulty = difficulty

    def next_guess(self):
        if not self.guess_words:
            return None
        max_score = 0
        for word in self.guess_words:
            score = self.score(word)
            if score > max_score:
                best_word = word
                max_score = score
        return best_word

    def initial_guess(self):
        pass

    def score(self, word):
        score = 0
        for position, letter in enumerate(word):
            exact_score = self.exact[letter][position]
            elsewhere_score = self.elsewhere[letter][position]
            absent_score = self.absent[letter]
            score += exact_score * elsewhere_score
            score += exact_score * absent_score
            score += elsewhere_score * absent_score
        return score

    def update_guess(self):
        pass

    def update_frequency(self):
        self.exact = {letter: [0]*self.word_length for letter in alphabet}
        self.elsewhere = {letter: [0]*self.word_length for letter in alphabet}
        self.present = {letter: 0 for letter in alphabet}
        list_length = 0
        for word in self.possible_words:
            list_length += 1
            for position, letter in enumerate(word):
                try:
                    self.exact[letter][position] += 1
                except IndexError:
                    print("Extra Long Word at:", word)
                    raise
                if letter not in word[position+1:]:
                    self.present[letter] += 1
                for other_position, other_letter in enumerate(word):
                    if letter != other_letter:
                        self.elsewhere[letter][other_position] += 1
        self.absent = {letter: list_length -
                       self.present[letter] for letter in alphabet}
        return self.exact, self.elsewhere, self.absent

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


def initial_filter(word_list, word_length):
    word_list = filter(lambda x: len(
        x) == word_length and x != '*'*word_length, word_list)
    return word_list


def pattern2key(pattern):
    return sum([value*2**index for index, value in enumerate(pattern)])


def key2pattern(key):
    index = 0
    pattern = []
    while key:
        pattern.append(key % 2 == 1)
        key = key//2
        index += 1
    return pattern


def calculate_frequency(word_list):
    assert word_list
    word_length = word_list[0]
    frequency = {letter: [0]*2**word_length for letter in alphabet}
    present = {letter: 0 for letter in alphabet}
    list_length = 0
    for word in word_list:
        list_length += 1
        for index, letter in enumerate(word):
            assert index < word_length
            if letter not in word[index+1:]:
                pattern = [letter == other_letter for other_letter in word]
                key = pattern2key(pattern)
                present[letter] += 1
                frequency[letter][key] += 1
    absent = {letter: list_length-present[letter] for letter in alphabet}
    for letter in alphabet:
        frequency[letter][0] = absent[letter]
    return frequency


def get_possibilities(word, letter):
    pattern = [ltr == letter for ltr in word]
    count = sum(pattern)
    short_possiblities = product(
        ["absent", "elsewhere", "exact"], repeat=count)
    possiblities = {}
    for short_possibility in short_possiblities:
        short_index = 0
        for pattern_index, pattern_bool in enumerate(pattern):
            if pattern_bool:
                assert pattern_index >= short_index
                possiblities[pattern_index] = short_possiblities[short_index]
                short_index += 1
            else:
                possiblities[pattern_index] = "unknown"
    return possiblities


def compare_patterns(target, guess):
    """
    [T, F, F], [T, F, F]
    [exact, unknown, unknown]
    [T, F, F], [F, T, F]
    [elsewhere, unknown, unknown]
    [T, T, F], [F, T, F]
    [absent, exact, unknown]
    """
    compared = ["unknown" for _ in target]
    for index, value in enumerate(target):
        if not value:
            compared[index] = "unknown"
        elif value == guess[index]:
            compared[index] = "exact"
        for guess_index, guess_value in enumerate(guess):
            if target[guess_index] = value and target[guess_index] != guess_value:
                compared[index] = "elsewhere"
                break
        else:
            compared[index] = "absent"
    return compared


def calculate_score(guess, guess_frequency):
    score = 0
    for word_index, letter in enumerate(guess):
        if letter not in word[guess+1:]:
            pattern = [ltr == letter for ltr in word]
            """
            guess_pattern[letter] = [T F F T F]
            patterns=target_frequency[letter]
            for pattern in patterns:
                
            """
            for
            guess_pattern = compare_guess(guess, pattern)
            guess_key = guess2key(guess_pattern)
            if guess_key in probability:
                probability[guess_key] += frequency[pattern]
            else:
                probability[guess_key] = frequency[pattern]
        for
    return score


"""
patterns can be: (1 or 0)^3
000
>[0][0][0]
>[0][0]{1}
>[0]{1}[0]
>[0]{1}{1}
>{1}[0][0]
>{1}[0]{1}
>{1}{1}[0]
>{1}{1}{1}
001
010
011
100
101
110
111
"""


def compare(target, guess):
    assert len(target) == len(guess)
    length = len(guess)
    clue = ['<'+str(char)+'>' for char in guess]
    for index in range(length):
        if target[index] == guess[index]:
            clue[index] = '['+str(guess[index])+']'
        elif guess[index] in clue:
            for target_value, guess_value in zip(list(target), list(guess)):
                if guess[index] == target_value and guess[index] != guess_value:
                    clue[index] = '('+str(guess[index])+')'
                    break
        else:
            clue[index] = '{'+str(guess[index])+'}'
    return "".join(clue)


def test_permutations(char_list, word_length):
    combo_list = list(product(char_list, repeat=word_length))
    return {target: {guess: compare(target, guess) for guess in combo_list} for target in combo_list}


def parse_guess(guess_string):
    pass


if __name__ == "__main__":
    clues = test_permutations([0, 1], 3)
    guesses = {guess[target]: clues[target][guess]
               for guess in clues for target in clues}
    for target in clues:
        print("target: "+str(target))
        print(clues[target])
"""
    targets = json_reader("targets.json")
    dictionary = json_reader("dictionary.json")
    word_length = 5
    targets = list(initial_filter(targets, word_length))
    dictionary = initial_filter(dictionary, word_length)
    solver = Solver(targets,dictionary,word_length)
    solver.update_frequency()
    guess=solver.next_guess()
    print(guess)
    print("exact: ")
    print(solver.exact)
    print("elsewhere: ")
    print(solver.elsewhere)
    print("present: ")
    print(solver.present)
    print("absent: ")
    print(solver.absent)
"""
