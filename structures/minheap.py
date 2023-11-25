"""
@package Heap

An implementation of heap and heap sort.

@function sorted(iterable=[], key=lambda x: x, reverse=False)
An overload of the built-in sorted function using the heap sort method

@class Heap(iterable=[], key=lambda x: x, reverse=False)
@Deprecating: using a key function instead of a dict means re-heapifying
              if the key is updated. Since this was originally for the
              a sorted method. The above refactor will remove the
              usefullness of this class.
A mutable queue that allows pushing and popping
"""

from collections.abc import Iterator

def sorted(iterable=[], key=lambda x: x, reverse=False):
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
        queue = _downheap(0, queue[1:], key, reverse)

    return sorted_list

def _downheap(i, queue, key, reverse):
    """
    Downheaps the i-th value of a heap.
    """
    parent = i
    while parent < len(queue):
        l_child = 2*parent+1
        r_child = 2*parent+2
        if l_child >= len(queue):
            # The queue is sorted if the parent has no children.
            return queue
        if r_child == len(queue):
            # If there is no right child use left the left child.
            child = l_child
        else:
            l_value = key(queue[l_child])
            r_value = key(queue[r_child])
            if not reverse:
                child = l_child if l_value > r_value else r_child
            else:
                child = l_child if l_value < r_value else r_child
        c_value = key(queue[child])
        p_value = key(queue[parent])
        if not reverse and p_value > c_value:
            # The heap condition is satisfied.
            return queue
        elif reverse and p_value < c_value:
            # The heap condition is satisifed.
            return queue
        else:
            temp = queue[child]
            queue[child] = queue[parent]
            queue[parent] = temp
            parent = child

class Heap(Iterator):
    """
    A more mutable heap queue for sorting iterables.

    i.e. for sorting and printing a list, similar to python's built-in
    sorted method.

    for i in HeapSequence(unsorted_list, key=lambda x: 1/x, reverse=True):
        print(i)
    """
    def __init__(self, iterable=[], key=lambda x: x, reverse=False):
        """
        Constructor for HeapSequence

        @param iterable: iterable to convert to a queue
                         default: empty queue
        @param key: A function defining the order of the sort
                    default: identity function
        @param reverse: Flag if the Heap should be reversed.
                    default: False
        """
        self._key = key
        self.reverse = reverse
        self.queue = list(iterable)
        self._heapify()

    def __next__(self):
        """
        Used to update the iterator. Raises a StopIteration exception
        when the queue is empty or calls pop when it is not.
        """
        if self.queue == []:
            raise StopIteration
        else:
            return self.pop()

    def cmp(self, x, y):
        """
        self.cmp(x, y) compares two items by value in queue.

        If [x, y] should be [y, x], it returns False. Otherwise it returns True
        """
        if self.reverse:
            return self.key(x) >= self.key(y)
        else:
            return self.key(x) <= self.key(y)

    def _heapify(self):
        """
        Transforms an unsorted self.queue into a heap.

        Used internally to re-apply the heap condition.
        """
        for i in reversed(range(len(self.queue))):
            # Traversing in reverse order allows the ability to skip
            # leaf nodes without calculating the index of that final node.
            self.downheap(i)

    def peek(self):
        """
        Returns the next value in queue.
        """
        return self.queue[0]

    def pop(self):
        """
        Removes and returns the next value in queue.
        """
        if len(self.queue) == 1:
            return self.queue.pop()
        else:
            next_item = self.queue[0]
            self.queue[0] = self.queue.pop()
            self.downheap(0)
            return next_item

    def push(self, value):
        """
        Adds a new value to the queue and restores the heap property.
        """
        self.queue.append(value)
        self._upheap(self.queue)

    def pushpop(self, value):
        """
        Adds a new value then returns the next value from the queue.  If
        the new value is higher priority then the value already next in
        queue, then the method just returns value.

        This runs faster than calling the individual push then pop methods.
        """
        if len(self.queue) == 0:
            return value
        elif self.cmp(value, self.queue[0]):
            return value
        else:
            next_item = self.queue[0]
            self.queue[0] = value
            self._downheap(0)
            return next_item

    def poppush(self, value):
        """
        Removes the next value in the queue then replaces that value
        with the provided argument.  Adds a new value then returns the
        next value from the queue.

        This runs faster than calling the individual push and pop methods.
        """
        next_value = self.queue[0]
        self.queue[0] = next_value
        return next_value

    def _downheap(self, index):
        while 2*index + 1 < len(self.queue):
            if len(self.queue) <= 2*index + 2:
                child = 2*index + 1
            elif self.cmp(self.queue[2*index+2], self.queue[2*index+1]):
                child = 2*index + 2
            else:
                child = 2*index + 1
            if self.cmp(self.queue[index], self.queue[child]):
                return
            else:
                temp = self.queue[child]
                self.queue[child] = self.queue[index]
                self.queue[index] = temp
                index = child

    def _upheap(self, index):
        while index != 0:
            parent = (index-1) // 2
            if self.cmp(self.queue[index], self.queue[parent]):
                return
            else:
                temp = self.queue[parent]
                self.queue[parent] = self.queue[index]
                self.queue[index] = temp
                index = parent

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, new_key):
        self._key = new_key

if __name__ == "__main__":
    print(sorted([3, 7, 8, 5, 2, 1, 9, 5, 4]))
