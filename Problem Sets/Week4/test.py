from contextlib import AbstractContextManager
from typing import Any
from my_queue import Queue
from my_stack import Stack
from unittest import TestCase, main

class TestQueue(TestCase):
    def setUp(self):
        self.queue = Queue()
        self.queue.enqueue(1)
        self.queue.enqueue(2)
        self.queue.enqueue(3)
        self.queue.enqueue(4)
    
    def test_getfront(self):
        self.assertEqual(self.queue.getFront(), 1)
    
    def test_getempty(self):
        self.queue = Queue()
        self.assertEqual(self.queue.getFront(), None)
    
    def test_dequeue(self):
        self.assertEqual(self.queue.dequeue(), 1)
        self.assertEqual(self.queue.dequeue(), 2)
        self.assertEqual(self.queue.dequeue(), 3)
        self.assertEqual(self.queue.dequeue(), 4)
        self.assertEqual(self.queue.dequeue(), None)

class TestStack(TestCase):
    def setUp(self):
        self.stack = Stack()
        self.stack.push(1)
        self.stack.push(2)
        self.stack.push(3)
        self.stack.push(4)
    
    def test_peek(self):
        self.assertEqual(self.stack.peek(), 4)
    
    def test_peekempty(self):
        self.stack = Stack()
        self.assertEqual(self.stack.peek(), None)
    
    def test_pop(self):
        self.assertEqual(self.stack.pop(), 4)
        self.assertEqual(self.stack.pop(), 3)
        self.assertEqual(self.stack.pop(), 2)
        self.assertEqual(self.stack.pop(), 1)
        self.assertEqual(self.stack.pop(), None)
    
if __name__ == '__main__':
    main()