import myinput,math

# **************************** read input **********************
# main_information = input()
# main_information = main_information.split(" - ")
# block_size = int(main_information[0])
# unified_or_separated = main_information[1]
# associativity = int(main_information[2])
# write_policy = main_information[3]
# write_miss_policy = main_information[4]
# # print(block_size)
# if unified_or_separated == '0':
#     unified_size = int(input().rstrip())
# else:
#     cache_size = input().rstrip().split(" - ")
#     instruction_cache_size = int(cache_size[0])
#     data_cache_size = int(cache_size[1])
#
# requests_line = []
# request = 'f'
# while( request != ''):
#     request = input().split()[:2]
#
#     # convert from base 16 to 10
#     request[1] = int(request[1], 16)
#     requests_line.append(request)

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

        self.occupied_size -= 1

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
            # print("one")
            return

        elif self.occupied_size < myinput.associativity:
            self.tail.next = block
            block.previous = self.tail
            self.tail = block
            self.occupied_size += 1
            # print("two")
            return
        else:
            self.DeleteAtStart()
            self.tail.next = block
            block.previous = self.tail
            self.tail = block
            # print(self.occupied_size)
            # print("three")
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
    if myinput.unified_or_separated == "0":
        number_of_misses = answer_requests_unified()
        return number_of_misses

def answer_requests_unified():

    number_of_misses = 0

    for request in myinput.requests_line:
        if request[0] == '0':
            number_of_misses += load_data(request)
        if request[0] == '1':
            number_of_misses += store_data(request)
    return number_of_misses

def load_data(request):

    number_of_misses = 0
    address_in_cache = int(int(request[1]) / myinput.block_size)
    set_number = int(address_in_cache % number_of_sets)
    tag = int(math.floor(address_in_cache / number_of_sets))
    target_set = Cache[set_number]
    valid = target_set.is_empty()
    if valid == False:
        number_of_misses = number_of_misses + 1
        new_block = Block(address_in_cache, tag)
        target_set.AddBlockToEnd(new_block)
    else:
        is_in_set = target_set.is_in_set(address_in_cache, tag)
        if is_in_set == True:
            block = Block(address_in_cache, tag)
            apply_LRU(target_set, block)
        else:
            number_of_misses += 1
            new_block = Block(address_in_cache, tag)
            target_set.AddBlockToEnd(new_block)
    # target_set.Print()
    # print("******")
    return number_of_misses

def store_data(request):
    pass

number_of_sets = int((myinput.unified_size / myinput.block_size) / myinput.associativity)

Cache = create_cache(number_of_sets)
for a in Cache:
    a.Print()
number_of_misses = answer_requests()
print(number_of_misses)
# print("***CACHE SETTINGS***")
# print("Unified I- D-cache")
# print("Size: {}".format(input.unified_size))
# print("Associativity: {}".format(associativity))
# print("Block size: {}".format(block_size))
# if write_policy == 'wb':
#     print("Write policy: WRITE BACK")
# else:
#     print("Write policy: WRITE THROUGH")
# if write_miss_policy == 'wa':
#     print("Allocation policy: WRITE ALLOCATE")
# else:
#     print("Allocation policy: WRITE NO ALLOCATE")
# print()
# print("***CACHE STATISTICS***")
# print("INSTRUCTIONS")
# print("accesses: 0")
# print("misses: 0")
# print("miss rate: 0.0000 (hit rate 0.0000)")
# print("replace: 0")
# print("DATA")
# print("accesses: ".format(len(requests_line)))
# print("misses: ".format(number_of_misses))
# miss_rate = format(round(number_of_misses/len(requests_line) , 4 ) , '.4f')
# hit_rate = format(round(1 - number_of_misses/len(requests_line) , 4 ) , '.4f')
# print("miss rate: {} (hit rate {})".format( miss_rate , hit_rate ))
# print("replace: 0")
# print("TRAFFIC (in words)")
# print("demand fetch: {}".format(int( (block_size*number_of_misses)/(4) )))
# print("copies back: 0")
#
