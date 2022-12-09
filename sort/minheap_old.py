class MinHeap:
	"""
	Queue implemented as a Min Heap Binary Tree
	"""
	def __init__(self):
		self._queue = []     # array of keys
		self._extracted = [] # previously opened keys
		self._values = {}    # dictionary mapping keys to weights
		self._indices = {}   # queue indices: key = self._queue[self._indices[key]]
	def __contains__(self, key):
		return key in self._values
	def __delitem__(self, key):
		del self._values[key] # need to clear previous weight in case it increases
		self.delete(key)
	def __getitem__(self, key):
		if key in self:
			return self._values[key]
		else:
			return self.__missing__(key)
	def __iter__(self):
		return self
	def __len__(self):
		return len(self._queue)
	def __missing__(self, key):
		return float('inf')
	def __bool__(self):
		return self._queue()
	def __next__(self):
		if self:
			return self.extract()
		else:
			raise StopIteration
	def __repr__(self):
		extracted_repr = ', '.join([repr(val)+': '+repr(self._values[val]) for val in self._extracted])
		queue_repr = ', '.join([repr(val)+': '+repr(self._values[val]) for val in self._queue])
		return '{'+extracted_repr+'| '+queue_repr+'}'
	def __setitem__(self, key, value):
		if key not in self:
			self.insert(key, value)
		elif self._values[key] > value:
			self.decrease_value(key, value)
		elif self._values[key] < value:
			self.increase_value(key, value)
	def __str__(self):
		return '{'+', '.join([str(val)+': '+str(self._values[val]) for val in self._extracted])+'}'
	def decrease_value(self, key, value):
		if key not in self:
			self.insert(key, value)
		elif self._values[key] > value:
			self._values[key] = value
			self._upheap(key)
	def increase_value(self, key, value):
		if key not in self:
			self.insert(key, value)
		elif self._values[key] > value:
			self._values[key] = value
			self._downheap(key)
	def insert(self, key, value):
		self._queue.append(key)
		self._values[key] = value
		self._indices[key] = len(self) - 1
		self._upheap(key)
	def delete(self, key):
		last = self._queue[-1]
		self._swap(key, last)
		next = self._queue.pop()
		parent = self.get_parent(last)
		if self._values[last] > self._values[parent]:
			self._upheap(last)
		else:
			self._downheap(last)
		return next
	def extract(self):
		first = self._queue[0]
		last = self._queue[-1]
		self._swap(first, last)
		next = self._queue.pop()
		self._extracted.append(next)
		self._downheap(last)
		return next
	def _swap(self, first, other):
		first_index = self._indices[first]
		other_index = self._indices[other]
		self._queue[first_index] = other
		self._queue[other_index] = first
		self._indices[first] = other_index
		self._indices[other] = first_index
	def _upheap(self, key):
		parent = self.get_parent(key)
		if self._values[key] < self._values[parent]:
			self._swap(key, parent)
			self._upheap(key)
	def _downheap(self, key):
		left = self.get_left_child(key)
		right = self.get_right_child(key)
		child = left if self._values[left] > self._values[right] else right
		if self._values[key] > self._values[child]:
			self._swap(key, child)
			self._downheap(key)
	def get_parent(self, key):
		parent_index = (self._indices[key]-1)//2
		if parent_index > 0:
			return self._queue[parent_index]
		else:
			return key
	def get_left_child(self, key):
		child_index = (2*self._indices[key])+1
		if child_index < len(self):
			return self._queue[child_index]
		else:
			return key
	def get_right_child(self, key):
		child_index = (2*self._indices[key])+1
		if child_index < len(self):
			return self._queue[child_index]
		else:
			return key
