import math

# **************************** read input **********************
main_information = input()
main_information = main_information.split(" - ")
block_size = int(main_information[0])
unified_or_separated = main_information[1]
associativity = int(main_information[2])
write_policy = main_information[3]
write_miss_policy = main_information[4]
# print(block_size)
if unified_or_separated == '0':
    unified_size = int(input().rstrip())
else:
    cache_size = input().rstrip().split(" - ")
    instruction_cache_size = int(cache_size[0])
    data_cache_size = int(cache_size[1])

requests_line = []
request = 'f'
while(True):
    request = input().split()[:2]
    if len(request) == 0:
        break
    # convert from base 16 to 10
    # print(request)
    request[1] = int(request[1], 16)
    requests_line.append(request)

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

        global copies_back
        global replace
        self.occupied_size -= 1

        if self.head == None:
            return
        current = self.head
        while current != None:
            if current.address == address and current.tag == tag:

                if current.dirty == 1:
                    copies_back += int(block_size/4)
                    # replace += 1
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
        global replace
        # global sizeOfSecondList
        if self.head is None:
            self.head = block
            self.tail = block
            block.previous = None
            self.occupied_size += 1
            # print("one")
            return

        elif self.occupied_size < associativity:
            self.tail.next = block
            block.previous = self.tail
            self.tail = block
            self.occupied_size += 1
            # print("two")
            return
        else:
            replace += 1
            self.DeleteAtStart()
            self.tail.next = block
            block.previous = self.tail
            self.tail = block
            # print(self.occupied_size)
            # print("three")
            return

    def make_dirty(self,given_address,given_tag):
        current = self.head
        while current != None:
            if current.address == given_address and current.tag == given_tag:
                current.dirty = 1
                return
            current = current.next
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
    if unified_or_separated == "0":
         answer_requests_unified()

    remain_dirty_blocks()

def answer_requests_unified():

    global number_of_misses

    for request in requests_line:
        if request[0] == '0' or request[0] == '2':
            load_data(request)
        if request[0] == '1':
            if write_policy == 'wb':
                write_back(request)
            else:
                 write_through(request)
    return

def load_data(request):

    global copies_back
    global demand_fetch
    global number_of_misses
    global replace

    address_in_cache = int(int(request[1]) / block_size)
    set_number = int(address_in_cache % number_of_sets)
    tag = int(math.floor(address_in_cache / number_of_sets))
    target_set = Cache[set_number]
    valid = target_set.is_empty()
    if valid == False:
        number_of_misses = number_of_misses + 1
        demand_fetch += int(block_size/4)
        new_block = Block(address_in_cache, tag)
        target_set.AddBlockToEnd(new_block)
    else:
        is_in_set = target_set.is_in_set(address_in_cache, tag)
        if is_in_set == True:
            block = Block(address_in_cache, tag)
            apply_LRU(target_set, block)
        else:
            number_of_misses += 1
            demand_fetch += int(block_size / 4)
            new_block = Block(address_in_cache, tag)
            target_set.AddBlockToEnd(new_block)
    # target_set.Print()
    # print("******")
    return

def write_back(request):

    global number_of_misses
    if write_miss_policy == 'wa':
         write_allocate(request)
    else:
         write_no_allocate(request)

def write_through(request):
    global number_of_misses
    if write_miss_policy == 'wa':
         write_allocate(request)
    else:
        pass

def write_allocate(request):

    global number_of_misses
    global copies_back
    global replace
    global demand_fetch

    address_in_cache = int(int(request[1]) / block_size)
    set_number = int(address_in_cache % number_of_sets)
    tag = int(math.floor(address_in_cache / number_of_sets))
    target_set = Cache[set_number]
    valid = target_set.is_empty()
    if valid == False:
        number_of_misses += 1
        demand_fetch += int(block_size/4)
        new_block = Block(address_in_cache, tag)
        if write_policy == 'wb':
            new_block.dirty = 1
        else:
            copies_back += 1
        target_set.AddBlockToEnd(new_block)
    else:
        is_in_set = target_set.is_in_set(address_in_cache, tag)
        if is_in_set == True:
            # replace += 1
            block = Block(address_in_cache, tag)
            apply_LRU(target_set, block)
            if write_policy == 'wb':
                copies_back -= int(block_size / 4)
            if write_policy == 'wb':
                target_set.make_dirty(address_in_cache,tag)
            else:
                copies_back += 1
        else:
            number_of_misses += 1
            demand_fetch += int(block_size / 4)
            new_block = Block(address_in_cache, tag)
            if write_policy == 'wb':
                new_block.dirty = 1
            else:
                copies_back += 1
            target_set.AddBlockToEnd(new_block)

def write_no_allocate(request):

    global number_of_misses
    global copies_back
    global replace
    if write_policy != 'wb':
        copies_back += 1

    address_in_cache = int(int(request[1]) / block_size)
    set_number = int(address_in_cache % number_of_sets)
    tag = int(math.floor(address_in_cache / number_of_sets))
    target_set = Cache[set_number]
    valid = target_set.is_empty()
    if valid == False:
        number_of_misses += 1
        if write_policy == 'wb':
            copies_back += 1
    else:
        is_in_set = target_set.is_in_set(address_in_cache, tag)
        if is_in_set == True:
            # replace += 1
            block = Block(address_in_cache, tag)
            apply_LRU(target_set, block)
            copies_back -= int(block_size/4)
            target_set.make_dirty(address_in_cache, tag)
        else:
            number_of_misses += 1
            if write_policy == 'wb':
                copies_back += 1
def remain_dirty_blocks():

    global copies_back
    for cache_set in Cache:
        current = cache_set.head
        while current != None:
            if current.dirty == 1:
                copies_back += int(block_size/4)
            current = current.next

number_of_sets = int((unified_size / block_size) / associativity)
copies_back = 0
number_of_misses = 0
demand_fetch = 0
replace = 0
Cache = create_cache(number_of_sets)
# for a in Cache:
#     a.Print()
answer_requests()

# print(demand_fetch)
# print(number_of_misses)
# print(copies_back)
# print(replace)
# print("***CACHE SETTINGS***")
# print(requests_line)
print("***CACHE SETTINGS***")
print("Unified I- D-cache")
print("Size: {}".format(unified_size))
print("Associativity: {}".format(associativity))
print("Block size: {}".format(block_size))
if write_policy == 'wb':
    print("Write policy: WRITE BACK")
else:
    print("Write policy: WRITE THROUGH")
if write_miss_policy == 'wa':
    print("Allocation policy: WRITE ALLOCATE")
else:
    print("Allocation policy: WRITE NO ALLOCATE")
print()
print("***CACHE STATISTICS***")
print("INSTRUCTIONS")
print("accesses: 0")
print("misses: 0")
print("miss rate: 0.0000 (hit rate 0.0000)")
print("replace: 0")
print("DATA")
print("accesses: {}".format(len(requests_line)))
print("misses: {}".format(number_of_misses))
miss_rate = format(round(number_of_misses/len(requests_line) , 4 ) , '.4f')
hit_rate = format(round(1 - number_of_misses/len(requests_line) , 4 ) , '.4f')
print("miss rate: {} (hit rate {})".format( miss_rate , hit_rate ))
print("replace: {}".format(replace))
print("TRAFFIC (in words)")
print("demand fetch: {}".format(int( demand_fetch )))
print("copies back: {}".format(copies_back))

