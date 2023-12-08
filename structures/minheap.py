"""
A queue package for lazy A* programmers.

Once a node has been popped it cannot be requeued.
With reverse=True (the default), lowest priority values are the first to pop out.

Typical usage:
queue = Queue({start_node, 0}, reverse=True)
for node in queue:
    # Do something with your newly popped node.
    # Then update the queue
    neighbors = {n: heuristic(n)+d for n, d in node.get_edges()}
    queue.update(neighbors)
    # or update the values individually.
    for n, d in node.get_edges():
        queue[n] = heuristic(n) + d
"""

from collections.abc import Iterator
from math import inf

class Queue(Iterator):
    """
    Queue() -> new empty queue
    Queue(mapping) -> new queue with mapping.keys() enqueued and
        mapping.values() as priority.
    Queue(..., reverse=True) -> setup queue as a min heap.
    """

    def __init__(self, mapping={}, /, reverse=True):
        """
        Initialize self. See help(type(self)) for more info.
        """
        self.priority = dict(mapping)
        self.queue = list(self.priority.keys())
        self.reverse = reverse
        for i in reversed(range(len(self.queue))):
            self._downheap(i)

    def __getitem__(self, key, /):
        """
        Gets the priority of a key if it has been set (even if it has
        been popped), otherwise return inf.
        """
        if key in self.priority:
            return self.priority[key]
        else:
            return inf

    def __next__(self, /):
        """
        Pops the next key from the queue and reapplies the heap property.
        """
        if self.queue:
            self.queue[0], self.queue[-1] = self.queue[-1], self.queue[0]
            next_key = self.queue.pop()
            self._downheap(0)
            return next_key
        else:
            raise StopIteration

    def __setitem__(self, key, value, /):
        """
        Updates the priority of a key or inserts key if it has not yet
        been queued.

        If key has already been popped, do nothing.
        """
        if key not in self.priority:
            self.queue.append(key)
            self.priority[key] = value
            self._upheap(len(self.queue) - 1)
        elif self.priority[key] > value:
            self.priority[key] = value
            for i, k in enumerate(self.queue):
                if key == k:
                    self._upheap(i)
        elif self.priority[key] < value:
            self.priority[key] = value
            for i, k in enumerate(self.queue):
                if key == k:
                    self._downheap(i)

    def update(self, mapping, /):
        """
        Skips any keys in mapping.keys() that have already been popped
        from queue.  Adds the keys from mapping.keys() that haven't been
        added to the queue.  Re-prioritizes any remaining key from
        mapping.keys() based on mapping[key].
        """
        for key, value in dict(mapping).items():
            self[key] = value

    def _upheap(self, i, /):
        """
        Upheaps the i-th value in heap.
        """
        child = i
        while child > 0:
            parent = (child-1) // 2
            p_priority = self.priority[self.queue[parent]]
            c_priority = self.priority[self.queue[child]]
            if self.reverse and p_priority <= c_priority:
                # Heap property has been satisified.
                return
            elif not self.reverse and p_priority >= c_priority:
                # Heap property has been satisified.
                return
            else:
                self.queue[child], self.queue[parent] = self.queue[parent], self.queue[child]
                child = parent

    def _downheap(self, i, /):
        """
        Downheaps the i-th value in heap.
        """
        parent = i
        while parent < len(self.queue):
            l_child = 2*parent + 1
            r_child = 2*parent + 2
            if l_child >= len(self.queue):
                # The heap condition is satisfied if there are no children.
                return
            if r_child == len(self.queue):
                # If there is no right child use left the left child.
                child = l_child
            else:
                # Choose the child that will be the new parent of the other.
                l_priority = self.priority[self.queue[l_child]]
                r_priority = self.priority[self.queue[r_child]]
                if self.reverse:
                    child = l_child if l_priority <= r_priority else r_child
                else:
                    child = l_child if l_priority >= r_priority else r_child
            p_priority = self.priority[self.queue[parent]]
            c_priority = self.priority[self.queue[child]]
            if self.reverse and p_priority <= c_priority:
                # Heap property has been satisified.
                return
            elif not self.reverse and p_priority >= c_priority:
                # Heap property has been satisified.
                return
            else:
                self.queue[child], self.queue[parent] = self.queue[parent], self.queue[child]
                parent = child
