(letrec ((bubble-tail
          (lambda (unsorted compare? sorted swap?)
            ; compare? is a lambda expression that evaluates true if a value should be before another.   
            ; swap? is true if a change to the order has happened during the last pass.                  
            (cond
             ((null? unsorted)
              ; if two values have been swapped restart otherwise return sorted                          
	      (if swap? sorted (bubble-tail (reverse sorted) compare? '() #t)))
             ((null? (cdr unsorted))
              (bubble-tail (cdr unsorted) compare? (cons (car unsorted) sorted) swap?))
             ((compare? (car unsorted) (cadr unsorted)) ; this isn't clear                               
	      (bubble-tail
	       (cons (car unsorted) (cddr unsorted))
	       compare?
	       (cons (cadr unsorted) sorted) #f))
             (else ; else if the current value is in the correct position                                
	      (bubble-tail (cdr unsorted) compare? (cons (car unsorted) sorted) swap?)))))
         (bubble-sort (lambda (unsorted compare?) (bubble-tail unsorted compare? '() #t))))
  (newline)
  (display "(bubble-sort '(3 7 8 5 2 1 9 5 4) <)\n")
  (display (bubble-sort '(3 7 8 5 2 1 9 5 4) <))
  (newline))
