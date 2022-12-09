(letrec
    ((split-half
      (lambda (unsplt lst1 lst2)
	(cond
	 ((null? unsplt) (list lst1 lst2))
	 ((null? (cdr unsplt)) (list (append unsplt lst1) lst2))  
	 (else (split-half (cddr unsplt) (cons (car unsplt) lst1) (cons (cadr unsplt) lst2))))))
     (split
      (lambda (unsplt)
	(cond
	 ((null? (cdr unsplt)) unsplt)
	 (else (map split (split-half unsplt '() '()))))))
     (merge
      (lambda (lst1 lst2 merged compare?)
	(cond
	 ((and (null? lst1) (null? lst2)) merged)
	 ((null? lst1)
	  (merge '() (cdr lst2) (cons (car lst2) merged) compare?))
	 ((null? lst2)
	  (merge (cdr lst1) '() (cons (car lst1) merged) compare?))
	 ((list? (car lst1))
	  (merge (reverse (merge (car lst1) (cadr lst1) '() compare?)) lst2 merged compare?))
	 ((list? (car lst2))
	  (merge lst1 (reverse (merge (car lst2) (cadr lst2) '() compare?)) merged compare?))
	 ((compare? (car lst1) (car lst2))
	  (merge (cdr lst1) lst2 (cons (car lst1) merged) compare?))
	 (else
	  (merge lst1 (cdr lst2) (cons (car lst2) merged) compare?)))))
     (merge-sort
      (lambda (unsorted compare?)
	((lambda (splt) (reverse (merge (car splt) (cadr splt) '() compare?)))
	 (split unsorted)))))
  (newline)
  (display "(merge-sort '(3 7 8 5 2 1 9 5 4) <)\n")
  (display (merge-sort '(3 7 8 5 2 1 9 5 4) <))
  (newline))
