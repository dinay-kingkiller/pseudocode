(letrec
    ((select-tail
      (lambda (checked unchecked sorted lowest compare?)
	(cond
	 ((null? unchecked)
	  (if (null? checked)
	      (cons lowest sorted)
	      (select-tail '() (cdr checked) (cons lowest sorted) (car checked) compare?)))
	 ((compare? lowest (car unchecked))
	  (select-tail (cons lowest checked) (cdr unchecked) sorted (car unchecked) compare?))
	 (else
	  (select-tail (cons (car unchecked) checked) (cdr unchecked) sorted lowest compare?)))))
     (select-sort
      (lambda (lst compare?)
	(if (null? lst) '() (select-tail '() (cdr lst) '() (car lst) compare?)))))
  (newline)
  (display "(select-sort '(3 7 8 5 2 1 9 5 4) <)\n")
  (display (select-sort '(3 7 8 5 2 1 9 5 4) <))
  (newline))
