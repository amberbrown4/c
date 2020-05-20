import codecs
requests_line = []
with codecs.open("2.trace","r","UTF8") as inputFile:
    inputFile = inputFile.readlines()

main_information = inputFile[0].rstrip().split(" - ")
block_size = int(main_information[0])
unified_or_separated = main_information[1]
associativity = int(main_information[2])
write_policy = main_information[3]
write_miss_policy = main_information[4]

if unified_or_separated == '0':
    unified_size = int(inputFile[1].rstrip())
else:
    cache_size = inputFile[1].rstrip().split(" - ")
    instruction_cache_size = int(cache_size[0])
    data_cache_size = int(cache_size[1])
for line in inputFile[2:]:
    request = line.rstrip().split()[:2]
    requests_line.append(request)
print(main_information)
print(requests_line)
# print(instruction_cache_size)