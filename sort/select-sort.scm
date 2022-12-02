(define (my-select-sort lst fun)
  (define (select-tail checked unchecked sorted lowest)
    (cond
     ((null? unchecked)
      (if (null? checked)
	  (cons lowest sorted)
	  (select-tail '() (cdr checked) (cons lowest sorted) (car checked))))
     ((> lowest (car unchecked)) (select-tail (cons lowest checked) (cdr unchecked) sorted (car unchecked)))
     (else (select-tail (cons (car unchecked) checked) (cdr unchecked) sorted lowest))))
  (if (null? lst) '() (reverse (select-tail '() (cdr lst) '() (car lst)))))

(display "(my-select-sort '(3 7 8 5 2 1 9 5 4) values)\n")
(display (my-select-sort '(3 7 8 5 2 1 9 5 4) values)) (newline) (newline)
