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
    def AddNodeToEnd(self,node):
        global sizeOfSecondList
        newNode = node
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
    def AddNodeToStart(self,node):
        global sizeOfSecondList

        newNode = node
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

    def Print(self):
        p = self.head
        while p != None:
            print(p.address,p.tag)
            p = p.next
    def ReversePrint(self):
        p = self.tail
        while p != None:
            print(p.data, end=" ")
            p = p.previous

class Cache_Set(LinkedList):
    def __init__(self,number):
        super().__init__()
        self.next = None
        self.previous = None
        self.number = number
    def DeleteBlock(self,address,tag):

        if self.head == None:
            return
        current = self.head
        while current != None:
            if current.address == address and current.tag == tag:
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

# class Cache(LinkedList):
#     def __init__(self,number_of_sets):
#         super().__init__()
#         self.number_of_sets = number_of_sets
#         # if self.head is None:
#         firtSet = Cache_Set(0)
#         block = Block(0, 2)
#         firtSet.AddNodeToEnd(block)
#         firtSet.Print()
#         self.head = firtSet
#         self.tail = firtSet
#         for i in range(1,self.number_of_sets):
#             new_set = Cache_Set(i)
#             block = Block(i, 2)
#             new_set.AddNodeToEnd(block)
#             self.tail.next = new_set
#             new_set.previous = self.tail
#             self.tail = new_set
#                 # newNode.previous = None
#                 # sizeOfSecondList += 1
#                 # return
#             # else:
#             #     self.tail.next = newNode
#             #     newNode.previous = self.tail
#             #     self.tail = newNode
#         # for i in range(self.number_of_sets):
#         #     cache_set = Cache_Set()
#         #     block = Block(i,2)
#         #     cache_set.AddNodeToEnd(block)
#         #     self.AddNodeToEnd(cache_set)
#
#     def print_cache(self):
#         current = self.head
#         # print(current is None)
#         while current != Node:
#             if current is not None:
#                 current.Print()
#                 print()
#                 current = current.next
#             else:
#                 print("goh")
# number_of_sets = int((input.unified_size/input.block_size)/input.associativity)
def create_cache(number_of_sets):
    Cache = []
    for i in range(number_of_sets):
        new_set = Cache_Set(i)
        block = Block(i, 2)
        new_set.AddNodeToEnd(block)
        Cache.append(new_set)
    return Cache
Cache = create_cache(5)
for a in Cache:
    a.Print()
