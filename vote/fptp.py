def elect(ballot_box):
    """
    An algorithm for calculating the first-past-the-post (FPTP) winner.
    
    Arugments:
    ballot_box: an iterable of ordered lists of candidates
    """
    count = defaultdict(int)
    for ballot in ballot_box:
        count[ballot] += 1
    winners = {c for c in count if count[c] == max(count.values())}
    if len(winners) == 1:
        return winners[0]
