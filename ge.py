from utils import encrypt, get_parts, get_random_addresses, WAY, NUM_SETS
from cache import Cache 
import random
random.seed(42)

def chunks(l, n):
    n = max(1, n)
    return [l[i:i+n] for i in range(0, len(l), n)]

print ("GE proof of work")
print ("N  = {0}".format(WAY*NUM_SETS))
print ("Trivial O(N^2) will be 10^10, on a modern computer that will take around 100 seconds")
print ("Demonstrating working of GE O(SW^2)")

target = get_random_addresses(1)[0]
(_, index, _) = get_parts(encrypt(target))

print ("Target address = {0} which maps to index {1}".format(bin(target), bin(index)))

sample_set = get_random_addresses()
ge_cache = Cache()
level = 0


while len(sample_set) > WAY:
    len_chunk = len(sample_set)//(WAY+1)

    groups = chunks(sample_set, len_chunk)

    happen = False 
    steps = 1
    for i, g in enumerate(groups):
        ge_cache.reset()
        ge_cache.add_to_cache(target)

        for j, gdash in enumerate(groups):
            if j == i:
                continue 
            
            for item in gdash:
                ge_cache.add_to_cache(item)
        
        if not ge_cache.check_hit(target):
            sample_set = []
            for j, gdash in enumerate(groups):
                if j == i:
                    continue
                sample_set += groups[j]
            
            happen = True 
            break
        steps +=1 

    level += 1
    if not happen:
        print ("Something is wrong")
        break 
    else:
        print ("At Level {0}, {1} steps were taken. New size of working set is {2}".format(level, steps, len(sample_set)))

print ("We have the eviction set")

for addr in sample_set:
    (_, index, _) = get_parts(encrypt(addr))
    print ("Address: {0} Index: {1}".format(bin(addr), bin(index)))
    
