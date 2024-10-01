# from linked_list import LinkedList
from typing import Any

class Queue:
    """
    A queue implementation using a linked list.
    
    The queue is a FIFO (First In, First Out) data structure.
    """

    def __init__(self) -> None:
        """
        Initialize a new Queue instance.
        """

    def enqueue(self, data) -> None:
        """
        Add an element to the rear of the queue.

        Parameters
        ----------
        data : Any
            The data to be added to the queue.
        """

    def dequeue(self) -> Any | None:
        """
        Remove and return the front element of the queue.

        Returns
        -------
        Any or None
            The data from the front of the queue, or None if the queue is empty.
        """

    def getFront(self) -> Any | None:
        """
        Return the front element of the queue without removing it.

        Returns
        -------
        Any or None
            The data from the front of the queue, or None if the queue is empty.
        """

    def isEmpty(self) -> bool:
        """
        Check if the queue is empty.

        Returns
        -------
        bool
            True if the queue is empty, False otherwise.
        """

if __name__ == "__main__":
    pass