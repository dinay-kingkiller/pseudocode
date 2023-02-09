from collections.abc import Collection, Iterator, Reversible


class Heap(Collection, Iterator):
    @classmethod
    def sort(cls, iterable, key=None, reverse=False):
        return list(Heap(iterable, key, reverse))

    def __init__(self, iterable, key=None, reverse=False):
        self.key = lambda x: x if key is None else key
        self.reverse = reverse
        self.queue = list(iterable)
        for i, _ in reversed(list(enumerate(self.queue))):
            """
            Transversing in reverse order allows the ability to skip
            leaf nodes without calculating the index of that final node.
            """
            self.downheap(i)

    def __bool__(self):
        return bool(self.queue)

    def __contains__(self, value):
        return value in self.queue

    def __len__(self):
        return len(self.queue)

    def __next__(self):
        if self.queue:
            return self.pop()
        else:
            raise StopIteration

    def cmp(self, x, y):
        """
        self.cmp(x, y) compares two items by value in queue.

        If [x, y] should be [y, x], it returns False. Otherwise it returns True
        """
        if self.reverse:
            return self.key(x) >= self.key(y)
        else:
            return self.key(x) <= self.key(y)

    def clear(self):
        self.queue.clear()

    def peek(self):
        return self.queue[0]

    def pop(self):
        if len(self) == 1:
            return self.queue.pop()
        else:
            next_item = self.queue[0]
            self.queue[0] = self.queue.pop()
            self.downheap(0)
            return next_item

    def push(self, value):
        """
        self.push adds the new value to the queue. The queue is then updated to maintain the heap property
        """
        self.queue.append(value)
        self.upheap(len(self))

    def pushpop(self, value):
        if len(self) == 0:
            return value
        elif self.cmp(value, self.queue[0]):
            return value
        else:
            next_item = self.queue[0]
            self.queue[0] = value
            downheap(0)
            return next_item

    def poppush(self, value):
        next_item = self.queue[0]
        self.queue[0] = value
        return next_item

    def downheap(self, index):
        while 2*index + 1 < len(self):
            if len(self) <= 2*index + 2:
                child = 2*index + 1
            elif self.cmp(self.queue[2*index+2], self.queue[2*index+1]):
                child = 2*index + 2
            else:
                child = 2*index + 1
            if self.cmp(self.queue[index], self.queue[child]):
                break
            else:
                temp = self.queue[child]
                self.queue[child] = self.queue[index]
                self.queue[index] = temp
                index = child

    def upheap(self, index):
        while index != 0:
            parent = (index-1) // 2
            if self.cmp(self.queue[index], self.queue[parent]):
                break
            else:
                temp = self.queue[parent]
                self.queue[parent] = self.queue[index]
                self.queue[index] = temp
                index = parent

    def to_tree(self, index):
        if 2*index + 2 < len(self):
            return [self.queue[index], self.to_tree(2*index + 1), self.to_tree(2*index + 2)]
        if 2*index + 1 < len(self):
            return [self.queue[index], self.to_tree(2*index + 1)]
        else:
            return [self.queue[index]]


if __name__ == "__main__":
    print(Heap.sort([3, 7, 8, 5, 2, 1, 9, 5, 4]))
