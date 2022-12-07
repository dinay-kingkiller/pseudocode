(letrec
    ((pivot-sublist
      (lambda (unsorted pivot lesser greater compare?)
	(cond
	 ((null? unsorted)
	  (cond
	   ((not (null? lesser))
	    (append
	     (pivot-sublist (cdr lesser) (car lesser) '() '() compare?)
	     (pivot-sublist greater pivot '() '() compare?)))
	   ((not (null? greater))
	    (cons pivot (pivot-sublist (cdr greater) (car greater) '() '() compare?)))
	   (else (list pivot))))
	 ((compare? pivot (car unsorted))
	  (pivot-sublist (cdr unsorted) pivot lesser (cons (car unsorted) greater) compare?))
	 (else
	  (pivot-sublist (cdr unsorted) pivot (cons (car unsorted) lesser) greater compare?)))))
     (pivot-sort
       (lambda (unsorted compare?)
	 (if (null? unsorted)
	     '()
	     (pivot-sublist (cdr unsorted) (car unsorted) '() '() compare?)))))
  (newline)
  (display "(pivot-sort '(3 7 8 5 2 1 9 5 4) <)\n")
  (display (pivot-sort '(3 7 8 5 2 1 9 5 4) <))
  (newline))
