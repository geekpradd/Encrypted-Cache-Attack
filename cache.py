from utils import *

class Cache:
    def __init__(self, tag_length=9, index_length=11, offset_length=12, way=16):
        self.cache = {}
        self.tag_length = tag_length
        self.index_length = index_length
        self.offset_length = offset_length
        self.ways = way

    def check_hit(self, address):
        encrypted = encrypt(address)

        (tag, index, offset) = get_parts(encrypted)

        if index in self.cache.keys():
            ind = -1
            data = self.cache[index]
            for i, j in enumerate(data):
                if j == tag:
                    ind = i 
                    break 
            
            if ind != -1:
                left = data[:ind]
                right = data[ind+1:]

                final = [tag] + left + right 
                self.cache[index] = final
                return True


        return False

    def add_to_cache(self, address):
        if not self.check_hit(address):
            encrypted = encrypt(address)

            (tag, index, offset) = get_parts(encrypted)

            if index in self.cache.keys():
                if len(self.cache[index]) == self.ways:
                    self.cache[index] = [tag] + self.cache[index][:-1]
                else:
                    self.cache[index] = [tag] + self.cache[index]
            else:
                self.cache[index] = [tag]

    def reset(self):
        self.cache = {}

