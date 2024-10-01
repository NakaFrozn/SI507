class Node:
    def __init__(self, data):
        self.data = data
        self.next = None # the pointer initially points to nothing as it is the end of the list
    def setNext(self, node):
        self.next = node
    def getNext(self) -> 'Node':
        return self.next
    def getData(self) -> 'Node':
        return self.data
    def __str__(self) -> str:
        return str(self.data)

class LinkedList:
    def __init__(self) -> None:
        self.head = None
    def append(self, Node) -> None:
        if self.head is None:
            self.head = Node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.setNext(Node)
    def replace(self, oldNodeData, newNodeData) -> None:
        newNode = Node(newNodeData)
        if self.head is None:
            return
        if self.head.data == oldNodeData:
            newNode.next = self.head.next
            self.head = newNode
        else:
            currentNode = self.head
            while currentNode.next is not None:
                if currentNode.next.data == oldNodeData:
                    newNode.next = currentNode.next.next
                    currentNode.next = newNode
                    return
                currentNode = currentNode.next

Node1 = Node(1)
Node2 = Node(2)
Node3 = Node(3)
Node1.setNext(Node2)
list1 = LinkedList()
list1.append(Node1)
