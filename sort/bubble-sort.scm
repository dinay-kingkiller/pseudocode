(letrec ((bubble-tail
	  (lambda (unsorted compare? sorted swap?)
	    ; compare? is a lambda expression that evaluates true if a value should be before another.
	    ; swap? is true if a change to the order has happened during the last run through
	    (cond
	     ((null? unsorted)
	      ; if two values have been swapped restart otherwise return sorted
	      (if swap? sorted (bubble-tail (reverse sorted) compare? '() #t)))
	     ((null? (cdr unsorted))
	      (bubble-tail (cdr unsorted) compare? (cons (car unsorted) sorted) swap?))
	     ((compare? (car unsorted) (cadr unsorted))
	      (bubble-tail
	       (cons (car unsorted) (cddr unsorted))
	       compare?
	       (cons (cadr unsorted) sorted) #f))
	     (else ; last value is in correct position
	      (bubble-tail (cdr unsorted) compare? (cons (car unsorted) sorted) swap?)))))
	 (my-bubble-sort (lambda (unsorted compare?) (bubble-tail unsorted compare? '() #t))))
  (newline)
  (display "(my-bubble-sort '(3 7 8 5 2 1 9 5 4) <)\n")
  (display (my-bubble-sort '(3 7 8 5 2 1 9 5 4) <))
  (newline))
