(letrec ((my-insert-sort (lambda (unsorted compare?) #t)))
  (newline)
  (display "(my-insert-sort '(3 7 8 5 2 1 9 5 4) <)\n")
  (display (my-insert-sort '(3 7 8 5 2 1 9 5 4) <))
  (newline))
