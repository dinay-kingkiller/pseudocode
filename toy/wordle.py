"""
A Wordle Solver v3

v1: tested each letter and position individually
v2: tested each letter and the pattern individually
v3: will check each word and generate the pattern difference
"""


from string import ascii_lowercase as alphabet

class Solver:
    def __init__(self, targets, guesses, word_length, difficulty="disjoint"):
        """
        targets: list of possible target words
        guesses: list of possible guess words
        word_length: word length to filter targets and guesses
        difficulty: how strict do guesses need to be
            disjoint = ignores any information from guesses and just eliminates any word with letters that have already been used in a guess.
            normal = any guess is permissible. Only zero information guesses are eliminated.
            hard = guess must
        """
        # Filter guesses to protect the algorithm
        self.word_length = word_length
        self.targets = [word for word in targets if len(word)==word_length]
        self.guesses = [word for word in guesses if len(world)==word_length]
    def __next__(self):
        """
        returns the next guess
        """
        # This allows disjoint to iterate through guesses
        if not self.guesses:
            raise StopIteration
            
        # update frequency
        self.frequency = {}
        for guess in self.guesses:
            self.frequency[guess] = {}
            for goal in self.targets:
                pattern = self.compare_words(guess, goal)
                key = self._guess_pattern2key(pattern)
                if key in self.frequency[guess]:
                    self.frequency[guess][key] += 1
                else:
                    self.frequency[guess][key] = 1
        
    
        max_score = 0
        for guess in self.guesses:
            score = self.score_word(guess)
            if score > max_score:
                max_score = score
                best_guess = guess
        return best_guess
    def score_word(self, guess):
        return self._poss_prod(self.frequency[guess].values())
    def compare_words(self, guess, target):
        """
        Compares a guess to a target word and returns information like Wordle.
        returns a pattern string:
            "exact": the guess and target letter match at that place
            "elsewhere": the guess letter is in the target, but not at that place
                It only sets this if the information from the target letter is not already used.
            "absent": any guess letters that remain
        """
        # Setup initial pattern with the exact matches
        pattern = ["exact" if x==y else "unknown" for x, y in zip(guess, target)]
        # Remove letters from guess as elsewhere should remove them
        target = [None if x=="exact" else y for x, y in zip(pattern, target)] 
        # 
        for guess_index, guess_letter in enumerate(guess):
            if guess_letter not in target:
                continue
            for target_index, target_letter in enumerate(target):
                if guess_letter == target_letter:
                    pattern[guess_index] = "elsewhere"
                    # break to eliminate only the first target_letter 
                    target[target_index] = None
                    break
        # Convert remaining "unknown" to "absent".
        pattern = ["absent" if x=="unknown" else x for x in pattern]
        return pattern
    def _letter_pattern2key(self, pattern):
        return sum([value*2**index for index, value in enumerate(reversed(pattern))])
    def _guess_pattern2key(self, pattern):
        converter = {"unknown":0, "absent":1, "elsewhere":2, "exact":3}
        return sum([converter[value]*4**index for index, value in enumerate(pattern)])
    def _key2letter_pattern(self, key):
        index = 0
        pattern = [False] * self.word_length
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
