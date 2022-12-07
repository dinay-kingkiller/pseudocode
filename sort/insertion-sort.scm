(letrec
    ((insertion-tail
      (lambda (sorted checked unsorted compare?)
	(cond
	 ((null? checked)
	  (if (null? unsorted)
	      sorted
	      (insertion-tail sorted (list (car unsorted)) (cdr unsorted) compare?)))
	 ((null? sorted)
	  (insertion-tail (list (car checked)) (cdr checked) unsorted compare?))
	 ((compare? (car sorted) (car checked))
	  (insertion-tail (cdr sorted) (cons (car checked) (cons (car sorted) (cdr checked))) unsorted compare?))
	 (else
	  (insertion-tail (append (reverse checked) sorted) '() unsorted compare?)))))
     (insertion-sort
      (lambda (unsorted compare?)
	(insertion-tail '() '() unsorted compare?))))
  (newline)
  (display "(insertion-sort '(3 7 8 5 2 1 9 5 4) <)\n")
  (display (insertion-sort '(3 7 8 5 2 1 9 5 4) <))
  (newline))
