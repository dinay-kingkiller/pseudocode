(newline)

(define (my-bubble-sort lst fun)
  (define (bubble-tail unsorted sorted sorted?)
    (cond
     ((null? unsorted)
      (if sorted? sorted (bubble-tail (reverse sorted) '() #t)))
     ((null? (cdr unsorted))
      (bubble-tail (cdr unsorted) (cons (car unsorted) sorted) sorted?))
     ((< (fun (car unsorted)) (fun (cadr unsorted)))
      (bubble-tail (cons (car unsorted) (cddr unsorted)) (cons (cadr unsorted) sorted) #f))
     (else
      (bubble-tail (cdr unsorted) (cons (car unsorted) sorted) sorted?))))
  (bubble-tail lst '() #t))

(display "(my-bubble-sort '(3 7 8 5 2 1 9 5 4) values)\n")
(display (my-bubble-sort '(3 7 8 5 2 1 9 5 4) values)) (newline) (newline)

(define (my-heap-sort lst fun) #t)
(define (my-insert-sort lst fun) #t)

(define (my-merge-sort lst)
  (define (split unsplt)
    (define (split-half unsplt lst1 lst2)
      (cond
       ((null? unsplt) (list lst1 lst2))
       ((null? (cdr unsplt)) (list (append unsplt lst1) lst2))
       (else (split-half (cddr unsplt) (cons (car unsplt) lst1) (cons (cadr unsplt) lst2)))))
    (cond
     ((null? (cdr unsplt)) unsplt)
     (else (map split (split-half unsplt '() '())))))
  (define (merge lst)
    (define (merge-tail lst1 lst2 merged)
      (cond
       ((and (null? lst1) (null? lst2)) merged)
       ((null? lst1) (merge-tail '() (cdr lst2) (cons (car lst2) merged)))
       ((null? lst2) (merge-tail (cdr lst1) '() (cons (car lst1) merged)))
       ((list? (car lst1)) (merge-tail (merge lst1) lst2 merged))
       ((list? (car lst2)) (merge-tail lst1 (merge lst2) merged))
       ((< (car lst1) (car lst2)) (merge-tail (cdr lst1) lst2 (cons (car lst1) merged)))
       (else (merge-tail lst1 (cdr lst2) (cons (car lst2) merged)))))
    (reverse (merge-tail (car lst) (cadr lst) '())))
  (merge (split lst)))

(display "(my-merge-sort '(3 7 8 5 2 1 9 5 4))\n")
(display (my-merge-sort '(3 7 8 5 2 1 9 5 4))) (newline) (newline)

(define (my-pivot-sort lst fun)
  (define (pivot-tail current left right)
    (cond
     ((null? current) '())
     ((null? (cdr current))
      (append (pivot-tail left '() '()) current (pivot-tail right '() '())))
     ((< (fun (car current)) (fun (cadr current)))
      (pivot-tail (cons (car current) (cddr current)) left (cons (cadr current) right)))
     (else
      (pivot-tail (cons (car current) (cddr current)) (cons (cadr current) left) right))))
  (pivot-tail lst '() '()))

(display "(my-pivot-sort '(3 7 8 5 2 1 9 5 4) values)\n")
(display (my-pivot-sort '(3 7 8 5 2 1 9 5 4) values)) (newline) (newline)

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
