from collections import defaultdict

def elect(ballot_box):
    """
    elect calculates and returns the Instant-Runoff Vote (IRV) winner for a ballot_box
    
    This algorithm uses "greedy elimination" to remove irrelevant ties.
    """
    eliminated = set()
    while ballot_box:
        # Counting Balllots
        count = defaultdict(int)
        for ballot in ballot_box:
            for candidate in ballot:
                if candidate in eliminated:
                    ballot.remove(candidate)
                    continue
                else:
                    # count only one candidate per ballot
                    count[candidate] += 1
                    break
            else:
                # remove empty ballots
                ballot_box.remove(ballot)
        sorted_candidates = [c in sorted(count, key=lambda c: count[c])]
        if len(sorted_candidates) == 1:
            return sorted_candidates[0]
        
        # Candidate Elimination
        for ranking, candidate in enumerate(sorted_candidates):
            # Greedy Elimination
            aggregate_count = sum([count[c] for c in sorted_candidates[ranking+1:]])
            if count[candidate] > aggregate_count:
                next_eliminated = set(sorted_candidates[ranking+1:])
                break
        else:
            # Single Elimination
            fewest_votes = min(count.values())
            next_eliminated = {c for c in count if count[c] == fewest_votes}
            if len(next_eliminated) != 1:
                return NotImplemented, "This ballot_box has an unhandled tie"
        eliminated |= next_eliminated
        
        
        
