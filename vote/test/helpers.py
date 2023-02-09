def ranked_to_choice(ballot):
    best_rank = min(ballot.values())
    winners = [candidate for candidate in ballot if ballot[candidate] == best_rank]
    if len(winners) == 1:
        return winners[0]
    else:
        return None


def scored_to_choice(ballot):
    best_score = max(ballot.values())
    winners = [
        candidate for candidate in ballot if ballot[candidate] == best_score]
    if len(winners) == 1:
        return winners[0]
    else:
        return None


def scored_to_ranked(scored_ballot):
    def _get_candidate_score(candidate): return scored_ballot[candidate]
    sorted_candidates = sorted(scored_ballot, key=_get_candidate_score)
    grouped_candidates = itertools.groupby(
        sorted_candidates, key=_get_candidate_score)
    return {candidate: rank for candidate in candidate_list for rank, candidate_list in enumerate(grouped_candidates)}


def strict_to_ranked(strict_ranked_ballots):
    def _order_to_ranking(ballot):
        return {candidate: ranking for ranking, candidate in enumerate(ballot)}
    return {elector: _order_to_ranking(ballot) for elector, ballot in strict_ranked_ballots}
