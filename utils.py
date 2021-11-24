import hashlib
OFFSET_BITS = 12
INDEX_BITS = 11 
TAG_BITS = 9
WAY = 16 
NUM_SETS = 2**INDEX_BITS

# 9 TAGS | 11 INDEX | 12 OFFSET

def encrypt(address):
    offset = address % (2**OFFSET_BITS)
    address = address//(2**OFFSET_BITS)
    index_value = (address) % (2**INDEX_BITS)
    tag = address//(2**INDEX_BITS)

    to_bytes = index_value.to_bytes(2, 'big')
    

    token = hashlib.sha256(to_bytes)

    value = int(token.hexdigest(), 16)

    new_index = (value//(2**OFFSET_BITS)) % (2**INDEX_BITS)

    encrypted = int((tag*(2**INDEX_BITS) + new_index)*(2**OFFSET_BITS) + offset)

    return encrypted

def get_parts(address):
    offset = address % (2**OFFSET_BITS)
    address = address//(2**OFFSET_BITS)
    index_value = (address) % (2**INDEX_BITS)
    tag = address//(2**INDEX_BITS)

    return (tag, index_value, offset)

def get_random_addresses(n = -1):
    if n == -1:
        n = NUM_SETS*WAY
    import random

    addreses = [x*2**(OFFSET_BITS) for x in random.sample(range(0, 2**(INDEX_BITS + TAG_BITS)), n)]

    return addreses




