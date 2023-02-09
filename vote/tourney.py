def elect(ballot_box, valid_candidates):
    """

    """
    count = dict.fromkeys(valid_candidates, 0)
    for ballot in ballot_box:
        # set any missing candidates to last place
        for candidate in valid_candidates:
            ballot.setdefault(candidate, len(valid_candidates))
        # invert the dict: score -> list of candidates
        scores = dict.fromkeys(ballot.values(), [])
        for candidate in valid_candidates:
            scores[ballot[candidate]] += [candidate]
        sorted_scores = sorted(scores, reverse=True)

        candidate_count = 0
        for score in sorted_score:
            new_candidates = scores[score]
            new_count = len(new_candidates)
            new_score = 2*candidate_count + new_count + 1
            for candidate in new_candidates:
                count[candidate] += new_score
            candidate_count += new_count
    winners = {c for c in count if count[c] == max(count.values())}
    if len(winners) == 1:
        return winners[0]
    else:
        raise NotImplemented, "This ballot_box has an unhandled tie"
