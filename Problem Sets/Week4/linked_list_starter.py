from typing import Any

class Node:
    """
    A node in a doubly linked list.

    Attributes
    ----------
    data : Any
        The data stored in the node.
    next : Node or None
        The next node in the linked list.
    prev : Node or None
        The previous node in the linked list.

    Parameters
    ----------
    data : Any, optional
        The data to be stored in the node (default is None).
    """
    
    def __init__(self, data = None) -> None:
        self.data = data
        self.next = None
        self.prev = None

class LinkedList:
    """
    A doubly linked list with dummy head and tail nodes to simplify node insertion and deletion.
    We require using dummyHead and dummyTail, since it will make certain implementation easier.
    Notice, the linked list is zero indexed.  

    Attributes
    ----------
    dummyHead : Node
        A dummy head node of the linked list.
    dummyTail : Node
        A dummy tail node of the linked list.
    size : int
        The number of elements in the linked list.

    Methods
    -------
    get(index)
        Retrieves the data at the specified index in the linked list.

    appendLeft(data)
        Adds a node with the given data at the beginning of the linked list.

    append(data)
        Adds a node with the given data at the end of the linked list.

    popLeft()
        Removes and returns the data from the beginning of the linked list.

    pop()
        Removes and returns the data from the end of the linked list.

    addAtIndex(index, data)
        Adds a node with the given data at the specified index in the linked list.

    deleteAtIndex(index)
        Deletes the node at the specified index from the linked list.

    printFromFront()
        Prints all elements of the linked list from front to back.

    printFromBack()
        Prints all elements of the linked list from back to front.

    _isNodeUnbound(node)
        Checks if the given node's linkage in the list is broken. 
        More specifically, check if the node is removed.

    getFront()
        Returns the data from the front (head) of the linked list.

    getBack()
        Returns the data from the back (tail) of the linked list.

    getSize()
        Returns the number of elements in the linked list.
    """

    def __init__(self) -> None:
        """
        Initializes a LinkedList instance with dummy head and tail nodes and sets size to zero.
        Notice data attribute of the dummyHead and dummyTail is None
        """
        self.dummyHead = Node(None)
        self.dummyTail = Node(None)
        self.dummyHead.next = self.dummyTail
        self.dummyTail.prev = self.dummyHead
        self.size = 0
    
    def get(self ,index: int) -> Any | None:
        """
        Retrieve the data at the specified index in the linked list.
        If the index is invalid, ie out of range, return None.


        Parameters
        ----------
        index : int
            The index of the node whose data is to be retrieved.

        Returns
        -------
        any or None
            The data at the specified index or None if index is invalid.
        """
        pass


    def appendLeft(self, data) -> None:
        """
        Create a new node, and assign the data to the new node.
        Add the node with the given data at the beginning of the linked list.
        Reset the positional relation(the next and prev attribute) of three
        related nodes.
        Increment the size by one.

        Parameters
        ----------
        data : any
            The data to be stored in the new node.

        Returns
        -------
        None
        """
        pass


    def append(self, data) -> None:
        """
        Add a node with the given data at the end of the linked list.
        Reset the positional relation(the next and prev attribute) of three
        related nodes.
        Increment the size by one.

        Parameters
        ----------
        data : any
            The data to be stored in the new node.

        Returns
        -------
        None
        """
        pass

    
    def popLeft(self) -> Any | None:
        """
        Remove and return the data from the beginning of the linked list.
        Decrease the size by one.
        Reset the positional relation(the next and prev attribute) of three
        related nodes.

        Returns
        -------
        any
            The data of the removed node, or None if the list is empty.

        None 
            If the linked list is empty.
        """
        pass


    def pop(self) -> Any | None:
        """
        Remove and return the data from the end of the linked list.
        Decrease the size by one.
        Reset the positional relation(the next and prev attribute) of three
        related nodes.

        Returns
        -------
        any
            The data of the removed node, or None if the list is empty.
        None 
            If the linked list is empty.
        """
        pass
            

    def addAtIndex(self, index: int, data: int) -> bool:
        """
        Add a node with the given data at the specified index in the linked list.
        You could assume the only illegal input is an out of range index. 
        Notice, you need to reset the connection at both side. 

        Parameters
        ----------
        index : int
            The index at which the new node should be inserted.
        data : any
            The data to be stored in the new node.

        Returns
        -------
        bool
            True if the addition was successful, False otherwise.
        """
        pass


    def deleteAtIndex(self, index: int) -> bool:
        """
        Delete a node with the given data at the specified index in the linked list.
        You could assume the only illegal input is an out of range index. 
        Notice, you need to reset the connection at both side. 

        Parameters
        ----------
        index : int
            The index at which the new node should be inserted.
        data : any
            The data to be stored in the new node.

        Returns
        -------
        bool
            True if the addition was successful, False otherwise.
        """
        pass


    def printFromFront(self) -> None:
        """
        Print all elements of the linked list from front to back,
        each element should be in a separate line. 
        If the linked list is empty, print exactly this string "Link list is empty."
        You should not include the value of dummy head or tail.

        Expected Output:
        firstElement  
        secondElement 
        ...
        """
        pass


    def printFromBack(self) -> None:
        """
        Prints all elements of the linked list from back to front.
        If the linked list is empty, print exactly this string "Link list is empty."
        Follow the same format of printFromFront()
        """
        pass


    def _isNodeUnbound(self,node) -> bool:
        """
        A private method. 
        Check if the given node's linkage in the list is broken.
        This means the node does not appear in the traversal from head to tail.
        In the other words, check if the connection relation between the node 
        and the node before it is neutral. 
        Notice this method assumes all the methods related to delete a node are 
        implemented correctly. 

        Parameters
        ----------
        node : Node
            The node to check for broken linkage.

        Returns
        -------
        bool
            True if the node's linkage is broken, False otherwise.

        Example
        --------
        check if the next attribute of the node's previous node is 
        the node.
        """
        pass

    
    def getFront(self) -> Any | None:
        """
        Returns the data from the first non dummy node in the linked list.

        Returns
        -------
        data or None
            The data of the first node in the list, or None if the list is empty.
        """
        pass

    def getBack(self) -> Any | None:
        """
        Returns the data from the last non dummy node in the linked list.

        Returns
        -------
        data or None
            The data of the last node in the list, or None if the list is empty.
        """
        pass
    
    def getSize(self) -> int:
        """
        Return the number of elements in the stack or queue.

        This method provides the current size of the linked list, 
        indicating how many elements are stored in it.

        Returns
        -------
        int
            The number of elements in linked list.
        """
        pass
        
"""
############################## Homework linked_list ##############################

% Student Name:

% Student Unique Name:

% Lab Section 00X: 

% I worked with the following classmates: 

%%% Please fill in the first 4 lines of this file with the appropriate information.
"""

if __name__ == "__main__":
    pass
