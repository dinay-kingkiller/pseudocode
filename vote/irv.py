from collections import defaultdict


def elect(ballot_box):
    """
    An algorithm for calculating the Instant-Runoff Vote (IRV) winner
    (also known as ranked-choice voting (RCV) in the United States or
    alternative vote (AV) in the United Kingdom).

    Note: This algorithm uses "greedy elimination" to remove irrelevant
    ties.

    Arugments:
    ballot_box: an iterable of ordered lists of candidates
    """
    eliminated = set()
    while ballot_box:
        # Counting Ballots
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

        ranked_candidates = [c in sorted(count, key=lambda c: count[c])]
        round_winner = ranked[0]
        if len(ranked_candidates) == 1:
            return round_winner

        for ranking, candidate in enumerate(ranked_candidates):
            # Greedy Elimination
            aggregate = sum([count[c] for c in ranked_candidates[ranking+1:]])
            if count[candidate] > aggregate:
                losers = set[ranked_candidates[ranking+1:])
                break
        else:
            # Single Elimination
            fewest_votes = min(count.values())
            losers = {c for c in count if count[c] == fewest_votes}
            if len(losers) != 1:
                raise NotImplemented, "This ballot_box has an unhandled tie"
        eliminated |= losers
