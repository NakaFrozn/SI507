class Queue:
    def __init__(self, data:list = []):
        self.data = data
        self.size = len(self.data)
    def append(self, item): # add an item to the tail
        self.data.append(item)
        self.size += 1
    def pop(self):
        if self.size == 0:
            return None
        self.size -= 1
        return self.data.pop(0) # remove and return the head of the queue
    def head(self, n:int = 1):
        if self.size == 0:
            return None
        if self.size < n:
            return self.data
        return self.data[:n] # return the first n elements of the queue
    def tail(self,n:int = 1):
        if self.size == 0:
            return None
        if self.size < n:
            return self.data
        return self.data[-n:] # return the last n elements of the queue
    def __str__(self):
        return str(self.data) # return the string of the data, make it printable

q = Queue([1,2,3,4,5])
print(q.pop())
print(q)
print(q.head(2))
print(q.tail(2))