import json
rarest_word = "murky"
def json_reader(filename):
    with open("targets.json",'r') as file:
        data=json.loads(file.read())
    return data
def initial_filter(word_list, word_length):
    word_list = filter(lambda x: len(x)==word_length and x!='*'*word_length, word_list)
    return word_list






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
    
