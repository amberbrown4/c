import input,math
class Node:
    def __init__(self):
        self.next = None
        self.previous = None

class Block(Node):
    def __init__(self,address,tag):
        super().__init__()
        self.address = address
        self.tag = tag
        # self.valid = 0
        self.dirty = 0

class LinkedList:
    def __init__(self):
        self.head = None
        self.tail= None

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
        self.occupied_size = 0

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

    def is_in_set(self,given_address,given_tag):
        current = self.head
        while current != None:
            if current.address == given_address and current.tag == given_tag:
                return True
            current = current.next
        return False

    def is_empty(self):
        if self.occupied_size == 0:
            return True
        else:
            False

    def AddBlockToEnd(self,block):
        # global sizeOfSecondList
        if self.head is None:
            self.head = block
            self.tail = block
            block.previous = None
            self.occupied_size += 1
            return

        elif self.occupied_size < input.associativity:
            self.tail.next = block
            block.previous = self.tail
            self.tail = block
            self.occupied_size += 1
            return
        else:
            self.DeleteAtStart()
            self.tail.next = block
            block.previous = self.tail
            self.tail = block
            return

def create_cache(number_of_sets):
    Cache = []
    for i in range(number_of_sets):
        new_set = Cache_Set(i)
        # block = Block(i, 2)
        # new_set.AddBlockToEnd(block)
        Cache.append(new_set)
    return Cache

def apply_LRU(cache_set,block):
    cache_set.DeleteBlock(block.address,block.tag)
    cache_set.AddBlockToEnd(block)

def answer_requests():
    number_of_misses = 0
    for request in input.requests_line:
        address_in_cache = int(int(request[1])/input.block_size)
        set_number = int(address_in_cache % number_of_sets)
        tag = int(math.floor(address_in_cache/ number_of_sets))
        target_set = Cache[set_number]
        valid = target_set.is_empty()
        if valid == False:
             number_of_misses = number_of_misses + 1
             new_block = Block(address_in_cache,tag)
             target_set.AddBlockToEnd(new_block)
        else:
            is_in_set = target_set.is_in_set(address_in_cache,tag)
            if is_in_set == True:
                block = Block(address_in_cache, tag)
                apply_LRU(target_set,block)
            else:
                number_of_misses += 1
                new_block = Block(address_in_cache, tag)
                target_set.AddBlockToEnd(new_block)
    return number_of_misses

number_of_sets = int((input.unified_size/input.block_size)/input.associativity)

Cache = create_cache(number_of_sets)
for a in Cache:
    a.Print()
number_of_misses = answer_requests()
print(number_of_misses)
