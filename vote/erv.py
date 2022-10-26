def elect(ballot_box, valid_candidates):
    """
    An alternative to Instant-Runoff Voting, this algorithm eliminates
    the candidate least preferred first. With each round of elimination,
    it checks for winners. If one candidate has a majority, they become
    the majority_winner. If all other candidates are eliminated they
    become the elimination_winner. Sometimes these are not equal: finding
    a majority is not a shortcut to the elimination winner like it is
    for IRV. If there is a tie after a majority is reached, but before
    the elimination winner is decided, the algorithm returns just the
    majority winner.
    
    Returns:
    majority_winner, elimination_winner, if both exist or else
    majority_winner, None
    
    
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
