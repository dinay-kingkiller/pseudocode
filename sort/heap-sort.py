from collections.abc import Iterator
class Heap(Iterator):
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
    def pop(self):
        if len(self.queue) == 1:
            return self.queue.pop()
        else:
            next_item = self.queue[0]
            self.queue[0] = self.queue.pop()
            self.downheap(0)
            return next_item
    def downheap(self, index):
        while 2*index + 1 < len(self.queue):
            if len(self.queue) <= 2*index + 2:
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
if __name__=="__main__":
    print("\nHeap.sort([3, 7, 8, 5, 2, 1, 9, 5, 4])")
    print(Heap.sort([3, 7, 8, 5, 2, 1, 9, 5, 4]),"\n")
