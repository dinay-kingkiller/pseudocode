def elect(ballot_box, valid_candidates):
    """
    
    """
    ballot_size = len(valid_candidates)
    count = dict.fromkeys(valid_candidates, 0) 
    for ballot in ballot_box:
        score_card = defaultdict(lambda: ballot_size, ballot)
        encoded_score = defaultdict(list)
        for candidate in score_card:
            encoded_score[score_card[candidate]] += [candidate]
        sorted_score = sorted(encoded_score, reverse=True)
        count_score = 0
        for ballot_score in sorted_score:
            tied_candidates = encoded_score[ballot_score]
            tied_count = len(tied_candidates)
            tied_score = 2*count_score + tied_count + 1
            count_score += tied_count
            count += tied_score
    return
            
            
