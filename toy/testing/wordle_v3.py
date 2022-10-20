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
