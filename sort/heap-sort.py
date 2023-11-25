"""
@package heapsort

An implementation of heap sort.

@function heapsort(iterable=[], key=lambda x: x, reverse=False)
A function with the same signature as the built-in sorted function using
the heap sort method.
"""

def heapsort(iterable=[], key=lambda x: x, reverse=False):
    """
    A replacement for the built-in sorted function using the heap sort method.

    Returns a sorted list
    """
    queue = list(iterable)

    # Heapify queue.
    for i in reversed(range(len(queue))):
        queue = _downheap(i, queue, key, reverse)

    # Sort queue.
    sorted_list = [None] * len(queue)
    for i in range(len(queue)):
        sorted_list[i] = queue[0]
        queue = _downheap(0, queue[-1:] + queue[1:-1], key, reverse)

    return sorted_list

def _downheap(i, heap, key, reverse):
    """
    Downheaps the i-th value of a heap.
    """
    parent = i
    while parent < len(heap):
        l_child = 2*parent + 1
        r_child = 2*parent + 2
        if l_child >= len(heap):
            # The heap condition is satisfied if there are no children.
            return heap
        if r_child == len(heap):
            # If there is no right child use left the left child.
            child = l_child
        else:
            l_value = key(heap[l_child])
            r_value = key(heap[r_child])
            # Choose the child that will be the new parent of the other.
            if not reverse:
                child = l_child if l_value <= r_value else r_child
            else:
                child = l_child if l_value >= r_value else r_child
        c_value = key(heap[child])
        p_value = key(heap[parent])
        if not reverse and p_value <= c_value:
            # The heap condition is satisfied.
            return heap
        elif reverse and p_value >= c_value:
            # The heap condition is satisifed.
            return heap
        else:
            heap[child], heap[parent] = heap[parent], heap[child]
            parent = child

if __name__ == "__main__":
    print("heapsort([3, 7, 8, 5, 2, 1, 9, 5, 4])")
    print(heapsort([3, 7, 8, 5, 2, 1, 9, 5, 4]))
