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
    instruction_cache_size = 0
    data_cache_size = 0
else:
    instruction_cache_size,data_cache_size = map(int , input().split(" - "))
    unified_size = 0

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
    def __init__(self,address,tag,type):
        super().__init__()
        self.address = address
        self.tag = tag
        # self.valid = 0
        self.dirty = 0
        self.type = type

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
        global copies_back

        if self.head.dirty == 1:
            copies_back += int(block_size/4)

        if self.head == None:
            return
        elif self.head.next == None:
            self.head = None

            return
        self.head = self.head.next
        self.head.previous = None

    def DeleteAtEnd(self):
        global sizeOfSecondList
        global copies_back

        if self.tail.dirty == 1:
            copies_back += int(block_size/4)

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
    def __init__(self,type,number):
        super().__init__()
        self.next = None
        self.previous = None
        self.number = number
        self.type = type
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
                if current.dirty == 1 and current == self.head:
                    self.DeleteAtStart()
                    copies_back -= int(block_size/4)
                elif current.dirty == 1 and current == self.tail:
                    self.DeleteAtEnd()
                    copies_back -= int(block_size/4)
                else:
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

    def is_in_set(self,given_address,given_tag,type):
        current = self.head
        while current != None:
            if current.address == given_address and current.tag == given_tag and current.type == type:
                return True
            current = current.next
        return False

    def is_empty(self):
        if self.occupied_size == 0:
            return True
        else:
            False

    def AddBlockToEnd(self,block):

        global instruction_replace
        global data_replace

        # global sizeOfSecondList
        if self.head is None:
            # print("1: {}".format(block.address * 16))
            self.head = block
            self.tail = block
            block.previous = None
            self.occupied_size += 1
            # print("one")
            return

        elif self.occupied_size < associativity:
            # print("2: {}".format(block.address * 16))
            self.tail.next = block
            block.previous = self.tail
            self.tail = block
            self.occupied_size += 1
            # print("two")
            return
        else:
            if block.type == 'data':
                data_replace += 1
            else:
                # print("3: {}".format(block.address*16))
                instruction_replace += 1
            self.DeleteAtStart()
            self.tail.next = block
            block.previous = self.tail
            self.tail = block
            if self.head is None:
                self.head = self.tail
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
    def was_dirty(self,block):
        current = self.head
        while current != None:
            if current.address == block.address and current.tag == block.tag:
                if current.dirty == 1:
                    return True
                else:
                    return False
            current = current.next
        return False

def create_cache():
    Cache = []
    if unified_or_separated == '0':
        number_of_sets_unified = int((unified_size / block_size) / associativity)
        for i in range(number_of_sets_unified):
            new_set = Cache_Set('unified',i)
            # block = Block(i, 2)
            # new_set.AddBlockToEnd(block)
            Cache.append(new_set)
    else:
        number_of_sets_instruction = int((instruction_cache_size / block_size) / associativity)
        number_of_sets_data = int((data_cache_size / block_size) / associativity)
        instruction_cache = []
        for i in range(number_of_sets_instruction):
            new_set = Cache_Set('instruction',i)
            instruction_cache.append(new_set)
        data_cache = []
        for i in range(number_of_sets_data):
            new_set = Cache_Set('data',i)
            data_cache.append(new_set)
        Cache = [instruction_cache , data_cache]
    return Cache

def apply_LRU(cache_set,block):
    cache_set.DeleteBlock(block.address,block.tag)
    cache_set.AddBlockToEnd(block)

def answer_requests():
    if unified_or_separated == '0':
         answer_requests_unified()
    else:
        answer_requests_separated()

    remain_dirty_blocks()

def answer_requests_unified():

    global accesses_instruction
    global accesses_data
    for request in requests_line:
        # print(copies_back)
        if request[0] == '0':
            accesses_data += 1
            load_data(Cache,request)
        elif request[0] == '2':

            accesses_instruction += 1
            load_data(Cache,request)
        if request[0] == '1':
            accesses_data += 1
            if write_policy == 'wb':
                write_back(Cache,request)
            else:
                 write_through(Cache,request)
    return

def answer_requests_separated():
    global accesses_data
    global accesses_instruction

    for request in requests_line:
        if request[0] == '0':
            accesses_data += 1
            load_data(Cache[1], request)
        elif request[0] == '2':
            accesses_instruction += 1
            load_data(Cache[0], request)
        else:
            accesses_data += 1
            if write_policy == 'wb':
                write_back(Cache[1],request)
            else:
                 write_through(Cache[1],request)


def load_data(temp_cache,request):

    global copies_back
    global demand_fetch
    global number_of_misses_data
    global replace
    global number_of_misses_instructions

    address_in_cache = int(math.floor(request[1]) / block_size)
    set_number = int(address_in_cache % len(temp_cache))
    tag = int(math.floor(address_in_cache / len(temp_cache)))
    target_set = temp_cache[set_number]
    # print("{} => {}".format(address_in_cache*16, set_number))
    # print(target_set)
    not_valid = target_set.is_empty()
    if request[0] == '0':
        type = 'data'
    else:
        type = 'instruction'
    if not_valid == True:
        # print(address_in_cache*16)
        if request[0] == '0':
            number_of_misses_data += 1
            new_block = Block(address_in_cache, tag,'data')
        else:
            number_of_misses_instructions += 1
            new_block = Block(address_in_cache, tag,'instruction')
        demand_fetch += int(block_size/4)
        target_set.AddBlockToEnd(new_block)
    else:
        is_in_set = target_set.is_in_set(address_in_cache, tag,type)
        if is_in_set == True:
            if request[0] == '0':
                block = Block(address_in_cache, tag,'data')
            else:
                block = Block(address_in_cache, tag, 'instruction')
            if target_set.was_dirty(block) == True:
                block.dirty = 1
            apply_LRU(target_set, block)
        else:
            if request[0] == '0':
                number_of_misses_data += 1
                new_block = Block(address_in_cache, tag, 'data')
            else:
                # print('**')
                # print(address_in_cache*16)
                # print("++")
                number_of_misses_instructions += 1
                new_block = Block(address_in_cache, tag, 'instruction')

            demand_fetch += int(block_size / 4)
            target_set.AddBlockToEnd(new_block)
    # target_set.Print()
    # print("******")
    return

def write_back(temp_cache,request):

    global number_of_misses
    if write_miss_policy == 'wa':
         write_allocate(temp_cache,request)
    else:
         write_no_allocate(temp_cache,request)

def write_through(temp_cache,request):
    global number_of_misses
    if write_miss_policy == 'wa':
         write_allocate(temp_cache,request)
    else:
        write_no_allocate(temp_cache,request)

def write_allocate(temp_cache,request):

    global number_of_misses_data
    global copies_back
    global replace
    global demand_fetch

    address_in_cache = int(int(request[1]) / block_size)
    set_number = int(address_in_cache % len(temp_cache))
    tag = int(math.floor(address_in_cache / len(temp_cache)))
    target_set = temp_cache[set_number]
    not_valid = target_set.is_empty()
    if not_valid == True:
        number_of_misses_data += 1
        demand_fetch += int(block_size/4)
        new_block = Block(address_in_cache, tag,'data')
        if write_policy == 'wb':
            new_block.dirty = 1
        else:
            copies_back += 1
        target_set.AddBlockToEnd(new_block)
    else:
        is_in_set = target_set.is_in_set(address_in_cache, tag,'data')
        if is_in_set == True:
            block = Block(address_in_cache, tag,'data')
            apply_LRU(target_set, block)
            # if write_policy == 'wb':
            #     copies_back -= int(block_size / 4)
            if write_policy == 'wb':
                # print(address_in_cache * 16)
                target_set.make_dirty(address_in_cache,tag)
            else:
                copies_back += 1
        else:
            number_of_misses_data += 1
            demand_fetch += int(block_size / 4)
            new_block = Block(address_in_cache, tag,'data')
            if write_policy == 'wb':
                new_block.dirty = 1
            else:
                copies_back += 1
            target_set.AddBlockToEnd(new_block)

def write_no_allocate(temp_cache,request):

    global number_of_misses_data
    global copies_back
    global replace
    if write_policy != 'wb':
        copies_back += 1

    address_in_cache = int(int(request[1]) / block_size)
    set_number = int(address_in_cache % len(temp_cache))
    tag = int(math.floor(address_in_cache / len(temp_cache)))
    target_set = temp_cache[set_number]
    not_valid = target_set.is_empty()
    if not_valid == True:
        number_of_misses_data += 1
        if write_policy == 'wb':
            copies_back += 1
    else:
        is_in_set = target_set.is_in_set(address_in_cache, tag,'data')
        if is_in_set == True:
            # replace += 1
            block = Block(address_in_cache, tag,'data')
            apply_LRU(target_set, block)
            if write_policy == 'wb':
                target_set.make_dirty(address_in_cache, tag)
            # copies_back -= int(block_size/4)
        else:
            number_of_misses_data += 1
            if write_policy == 'wb':
                copies_back += 1
def remain_dirty_blocks():

    global copies_back
    if unified_or_separated == '0':
        cache = Cache
    else:
        cache = Cache[1]
    for cache_set in cache:
        current = cache_set.head
        while current != None:
            if current.dirty == 1:
                copies_back += int(block_size/4)
            current = current.next

copies_back = 0
number_of_misses_data = 0
number_of_misses_instructions = 0
demand_fetch = 0
instruction_replace = 0
data_replace = 0
accesses_instruction = 0
accesses_data = 0
Cache = create_cache()
# print(len(Cache))
# print(Cache)
# for a in Cache:
#     a.Print()
answer_requests()

# print(demand_fetch)
# print(number_of_misses)
# print(copies_back)
# print(replace)
# print("***CACHE SETTINGS***")
# print(requests_line)
# print(int(block_size/4))
print("***CACHE SETTINGS***")
if unified_or_separated == '0':
    print("Unified I- D-cache")
    print("Size: {}".format(unified_size))
else:
    print("Split I- D-cache")
    print("I-cache size: {}".format(instruction_cache_size))
    print("D-cache size: {}".format(data_cache_size))
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
print("accesses: {}".format(accesses_instruction))
print("misses: {}".format(number_of_misses_instructions))
if accesses_instruction != 0:
    miss_rate = format(round(number_of_misses_instructions/accesses_instruction , 4 ) , '.4f')
    hit_rate = format(round(1 - number_of_misses_instructions/accesses_instruction , 4 ) , '.4f')
else:
    miss_rate = '0.0000'
    hit_rate = '0.0000'
print("miss rate: {} (hit rate {})".format( miss_rate , hit_rate ))
print("replace: {}".format(instruction_replace))
print("DATA")
print("accesses: {}".format(accesses_data))
print("misses: {}".format(number_of_misses_data))
miss_rate = format(round(number_of_misses_data/accesses_data , 4 ) , '.4f')
hit_rate = format(round(1 - number_of_misses_data/accesses_data , 4 ) , '.4f')
print("miss rate: {} (hit rate {})".format( miss_rate , hit_rate ))
print("replace: {}".format(data_replace))
print("TRAFFIC (in words)")
print("demand fetch: {}".format(int( demand_fetch )))
print("copies back: {}".format(copies_back))

