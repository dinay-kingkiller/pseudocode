from collections import defaultdict


def elect(ballot_box):
    count = defaultdict(int)
    while ballot_box:
        for ballot in ballot_box:
            for candidate in ballot:
                if candidate in eliminated:
                    continue
                else:
                    count[candidate] += 1
            else:
                pass
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
