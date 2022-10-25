from collections import defaultdict
def elect(ballot_box):
    """
    An alternative to Instant-Runoff Voting, this algorithm eliminates the candidate with the most lowest rank votes
    
    Arugments:
    ballot_box: an iterable of ordered lists of candidates
    """
    while ballot_box:
        count = defaultdict(int)
        for ballot in ballot_box:
            ballot.pop()
