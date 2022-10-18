import itertools
from collections import defaultdict

def from_choice_ballots(choice_ballots, population = {}):
    """
    ballot_box = {elector:candidate}
    """
    new_ballot_box = BallotBox()
    new_ballot_box.add_ballot_box(ChoiceBallotBox(choice_ballots, population))
    new_ballot_box._add_attr(new_ballot_box.choice_ballot_box)
    return new_ballot_box
def from_ranked_ballots(ranked_ballots, population = {}):
    """
    ballot_box = {elector:{candidate0:rank0, candidate1:rank1, ...}}
    """
    new_ballot_box = BallotBox()
    if any(BallotBox.has_duplicates(ballot) for ballot in ranked_ballots.values()):
        raise ValueError, "Duplicate Ballot Found"
    choice_ballots = {elector:ranked_to_choice(ballot) for elector, ballot in ranked_ballots.items() if ballot != {}}
    if all(choice_ballots.values()):
        new_ballot_box.add_ballot_box(ChoiceBallotBox(choice_ballots, population))
    if all(is_strict_rank(ballot) for ballot in ranked_ballots.values()):
        new_ballot_box.ranked_ballot_box = StrictRankedBallotBox(ranked_ballots, population)
        new_ballot_box._add_attr(new_ballot_box.ranked_ballot_box)
    else:
        new_ballot_box.ranked_ballot_box = RankedBallotBox(ranked_ballots, population)
        new_ballot_box._add_attr(new_ballot_box.ranked_ballot_box)
    return new_ballot_box
def from_scored_ballots(cls, scored_ballots, population = {}):
    """
    ballot_box = {elector:{candidate0:score0, candidate1:score1, ...}}
    """
    pass
def from_strict_ranked_ballots(cls, strict_ranked_ballots, population = {}):
    """
    ballot_box = {elector:[candidate0, candidate1, ... ]}
    """
    new_ballot_box = cls()
    if any(cls._has_duplicates(ballot) for ballot in ranked_ballots.values()):
        raise ValueError, "Duplicate Ballot Found"
    ranked_ballots = cls._strict_to_ranked(strict_ranked_ballots)
    choice_ballots = cls._strict_to_choice(strict_ranked_ballots)
    new_ballot_box.choice_ballot_box = ChoiceBallotBox(choice_ballots, population)
    new_ballot_box.ranked_ballot_box = StrictRankedBallotBox(ranked_ballots, population)
    new_ballot_box._add_attr(new_ballot_box.choice_ballot_box)
    new_ballot_box._add_attr(new_ballot_box.ranked_ballot_box)
    return new_ballot_box
def is_strict_rank(ballot):
    ranks = ballot.values()
    return len(set(ranks))==len(ranks)
def is_strict_score(ballot):
    scores = ballot.values()
    return len(set(scores))==len(scores)
def has_duplicates(ballot):
    return any(len(candidate)!=len(set(candidate)) for candidate in ballot)
def has_best_rank(ballot):
    pass
def has_best_score(ballot):
    pass
def ranked_to_choice(ballot):
    best_rank = min(ballot.values())
    winners = [candidate for candidate in ballot if ballot[candidate]==best_rank]
    if len(winners)==1:
        return winners[0]
    else:
        return None
def scored_to_choice(ballot):
    best_score = max(ballot.values())
    winners = [candidate for candidate in ballot if ballot[candidate]==best_score]
    if len(winners)==1:
        return winners[0]
    else:
        return None
def scored_to_ranked(scored_ballot):
    _get_candidate_score = lambda candidate:scored_ballot[candidate]
    sorted_candidates = sorted(scored_ballot, key=_get_candidate_score)
    grouped_candidates = itertools.groupby(sorted_candidates, key=_get_candidate_score)
    return {candidate:rank for candidate in candidate_list for rank, candidate_list in enumerate(grouped_candidates)}
def strict_to_ranked(strict_ranked_ballots):
    def _order_to_ranking(ballot):
        return {candidate: ranking for ranking, candidate in enumerate(ballot)}
    return {elector: _order_to_ranking(ballot) for elector, ballot in strict_ranked_ballots}


class BallotBoxContainer(Object):
    """Ballot Box Container

    ...
    Attributes
    ----------
    ballot_boxes: [SomeBallotBox, SomeOtherBallotBox]
        list of ballot box objects: all with the same source data
    
    Methods
    -------
    add_ballot_box
        adds some ballot box object to container
    _add_methods
        private function to add 
    """
    def __init__(self, population):
        self.ballot_boxes = []
    def add_ballot_box(ballot_box):
        self.ballot_boxes.append(ballot_box)
        self._add_methods(ballot_box)
    def _add_methods(self, obj)
        all_names = dir(obj)
        for name in all_names:
            attr = getattr(obj, name)
            if callable(attr) and not name.startswith('_'):
                setattr(self, name, attr) 
class BallotBox:
    def __init__(self, ballots, population = {}):
        self.ballots = ballots
        self._population = defaultdict(lambda: 1, population)
    def _get_to_win(self, ballots):
        
    
class ChoiceBallotBox:
    """
    choice_ballots = {elector:candidate}
    """
    def __init__(self, choice_ballots, population = {}):
        self.ballots = choice_ballots
        self._population = defaultdict(lambda: 1, population)
    @property
    def fptp(self):
        pass
class RankedBallotBox:
    """
    ranked_ballots = {elector:{candidate0:rank0, candidate1:rank1, ...}}
    """
    def __init__(self, ranked_ballots, population = {}):
        self.ballots = ranked_ballots
        self._population = defaultdict(lambda: 1, population)
class ScoredBallotBox:
    """
    scored_ballots = {elector:{candidate0:score0, candidate1:score1, ...}}
    """
    def __init__(self, scored_ballots, population = {}):
        self.ballots = scored_ballots
        self._population = defaultdict(lambda: 1, population)
class StrictRankedBallotBox(RankedBallotBox):
    def full_irv(self):
        ballots = self.ballots.copy()
        self.eliminated_candidates = {}
        while ballots:
            electors = ballots.keys()
            to_win = sum(population for elector, value in self._population if key in electors)
            for elector, ballot in ballots:
                for candidate in sorted(ballot.keys(), key=lambda ):
                    if candidate in self.eliminated_candidates:
                        del ballot[candidate]
                        continue
                    elif candidate in count:
                         count[candidate] += self._population[elector]
                    else:
                        count[candidate] = self._population[elector]
                else:
                    ## delete exhausted ballots
                    del ballots[elector]
            eliminated_this_round = self._irv_thrifty_eliminated(count)
            self.eliminated_candidates[loser].update(eliminated_this_round)
    def _irv_thrifty_eliminated(vote_count):
        min_value = min(vote_count.values())
        low_count, high_count = self._split_by_value(vote_count)
        if len(low_count) == 1:
            return low_count
        while len(high_count)<=2:
            low_sum = sum(vote_count[candidate] for candidate in low_cand)
            next_low, next_high = self._split_by_min(high_cand)
            if len(next_low) > 1:
                ## this guard clause keeps us from eliminating too many for next_next
                low_count.update(next_low)
                continue
            next_next_low, _ = self._split_by_min(high_cand)
            next_min = list(next_low.values())[0]
            next_next_min = list(next_next_low.values())[0]
            low_count.update(next_low)
            if low_sum + next_min < next_next_min:
                return low_count
            else:
                low_count.update(low_count)
                continue
        else:
            raise NotImplementedError, "This Ballot Box has an unhandled tie"
    def _irv_greedy_eliminate(count):
        pass
    def _split_by_value(self, function, dictionary):
        def is_eq_value(item): item[1] == value
        def is_neq_value(item): item[1] != value
        true_dictionary = dict(filter(is_eq_value, dictionary.items()))
        false_dictionary = dict(filter(is_neq_value, dictionary.items())
        return true_dictionary, false_dictionary
    def _get_population(self, elector):
        return self._population[elector]
    ##Eliminate the candidate appearing as the first preference on the fewest ballots.
    ##If only one candidate remains, elect this candidate and stop.
    ##Otherwise go to 1.
class StrictScoredBallotBox(ScoredBallotBox):
    pass
