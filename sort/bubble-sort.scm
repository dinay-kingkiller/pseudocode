(letrec
    ((bubble-tail
      (lambda (unsorted sorted bubble compare? swap? reversed?)
        ; reversed? is used to bubble from both sides of the linked list
	(cond
	 ((null? unsorted) ; Has it finished a pass?
	  (cond
	   (swap? ; Has there been a swap in the last pass?
	    (bubble-tail sorted '() bubble (lambda (x y) (compare? y x)) #t (not reversed?)))
	   (reversed?
	    (reverse (cons bubble sorted)))
	   (else
	    (cons bubble sorted))))
	 ((null? sorted) ; Push bubble to sorted if its at the beginning of a pass
	  (bubble-tail (cdr unsorted) (list bubble) (car unsorted) compare? #f reversed?))
	 ((compare? bubble (car unsorted))
	  (bubble-tail (cdr unsorted) (cons (car unsorted) sorted) bubble compare? #t reversed?))
	 (else ; If the current value is in the correct position                                
	  (bubble-tail (cdr unsorted) (cons bubble sorted) (car unsorted) compare? swap? reversed?)))))
     (bubble-sort
      (lambda (unsorted compare?)
	(if (null? unsorted) '() (bubble-tail (cdr unsorted) '() (car unsorted) compare? #f #f)))))
  (newline)
  (display "(bubble-sort '(3 7 8 5 2 1 9 5 4) <)\n")
  (display (bubble-sort '(3 7 8 5 2 1 9 5 4) <))
  (newline))
