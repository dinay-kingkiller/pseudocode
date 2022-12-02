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
