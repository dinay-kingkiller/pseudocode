def elect(ballot_box, valid_candidates):
    """
    An alternative to Instant-Runoff Voting, this algorithm eliminates the candidate with the most lowest rank votes, then rechecks the remaining candidates
    
    Arugments:
    ballot_box: a list of ordered lists of candidates
    candidates: the list of valid candidates
    """
    eliminated = set()
    while ballot_box:
        # Counting Ballots
        count = dict.fromkeys(valid_candidates, 0)
        for ballot in ballot_box:
            for candidate in ballot:
                if candidate not in eliminated:
                    count[candidate] += 1
                    break
        sorted_candidates = [c in sorted(count, key=lambda c: count[c])]
        ### fix below this
        if len(sorted_candidates) == 1:
            return sorted_candidates[0]
        
        # Candidate Elimination
        for ranking, candidate in enumerate(sorted_candidates):
            # Greedy Elimination
            aggregate = sum([count[c] for c in sorted_candidates[ranking+1:]])
            if count[candidate] > aggregatet:
                next_eliminated = set(sorted_candidates[ranking+1:])
                break
        else:
            # Single Elimination
            fewest_votes = min(count.values())
            next_eliminated = {c for c in count if count[c] == fewest_votes}
            if len(next_eliminated) != 1:
                return NotImplemented, "This ballot_box has an unhandled tie"
        eliminated |= next_eliminated
