import input
class Node:
    def __init__(self):
        self.next = None
        self.previous = None

class Block(Node):
    def __init__(self,address,tag):
        super().__init__()
        self.address = address
        self.tag = tag
        self.valid = 0
        self.dirty = 0

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail= None
    def AddNodeToEnd(self,block):
        global sizeOfSecondList
        newNode = block
        if self.head is None:
            self.head = newNode
            self.tail = newNode
            newNode.previous = None
            # sizeOfSecondList += 1
            return
        else:
            self.tail.next = newNode
            newNode.previous = self.tail
            self.tail = newNode
    def AddNodeToStart(self,block):
        global sizeOfSecondList

        newNode = block
        if self.head == None:
            self.head = newNode
            self.tail = newNode
            return
        newNode.next = self.head
        self.head.previous = newNode
        self.head = newNode

    def DeleteAtStart(self):
        global sizeOfSecondList

        if self.head == None:
            return
        elif self.head.next == None:
            self.head = None

            return
        self.head = self.head.next
        self.head.previous = None

    def DeleteAtEnd(self):
        global sizeOfSecondList

        if self.head == None:
            return
        elif self.head.next == None:
            self.head = None

            return
        (self.tail.previous).next = None
        self.tail = self.tail.previous

    def DeleteNode(self,address,tag):
        if self.head == None:
            return
        current = self.head
        while current != None:
            if current.data == :
                if current == self.head:
                    self.DeleteAtStart()
                elif current == self.tail:
                    self.DeleteAtEnd()
                else:
                    current.previous.next = current.next
                    current.next.previous = current.previous
                return
            current = current.next
        return None

    def Print(self):
        p = self.head
        while p != None:
            print(p.data,end=" ")
            p = p.next
    def ReversePrint(self):
        p = self.tail
        while p != None:
            print(p.data, end=" ")
            p = p.previous
class Cache_Set(LinkedList):
        pass
class Cache(LinkedList):
    def search(self):
        current = self.head
        while current != Node:
            if current.
number_of_sets = int((input.unified_size/input.block_size)/input.associativity)
print(number_of_sets)
for