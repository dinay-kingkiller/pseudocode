def elect(ballot_box, valid_candidates):
    """
    An alternative to Instant-Runoff Voting, this algorithm eliminates the candidate with the most lowest rank votes, then rechecks the remaining candidates
    
    Returns majority winner or (majority winner
    
    Arugments:
    ballot_box: a list of ordered lists of candidates
    candidates: the list of valid candidates
    """
    eliminated = set()
    to_win = len(ballot_box) // 2
    majority_winner = None
    while ballot_box:
        # Counting Ballots
        count = defaultdict(int)
        for ballot in ballot_box:
            assert set(ballot) == set(valid_candidates)
            for candidate in ballot:
                if candidate not in eliminated:
                    count[candidate] += 1
                    break
                    
        ranked = [c in sorted(count, key=lambda c: count[c])]
        round_winner = ranked[0]
        if count[round_winner] > to_win:
            majority_winner = round_winner
        if len(ranked) == 1:
            elimination_winner = round_winner
            return majority_winner, elimination_winner
        
        fewest_votes = min(count.values())
        round_losers = {c for c in count if count[c] == fewest_votes}
        if len(round_losers) == 1:
            eliminated |= round_losers
        if majority_winner:
            return majority_winner, None
        if len(round_losers) != 1:
            raise NotImplemented, "This ballot_box has an unhandled tie."
