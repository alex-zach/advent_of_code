import re

from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('1320', '145'))
    
    def parse_input(self, lines):
        return lines[0].strip().split(',')

    def aoc_hash(self, str):
        res = 0
        for c in str:
            res += ord(c)
            res *= 17
            res %= 256
        return res

    def solve1(self, init_sequence):
        return sum(self.aoc_hash(s) for s in init_sequence)

    def solve2(self, init_sequence):
        init_sequence = list(map(lambda x: (x.split('=')[0], int(x.split('=')[1])) if '=' in x else (x[0:-1], '-'), init_sequence))
        hashmap = {i: [] for i in range(256)}
        focusmap = {}

        for label, op in init_sequence:
            label_hash = self.aoc_hash(label)
            if op == '-':
                if label in hashmap[label_hash]: 
                    hashmap[label_hash].remove(label)
                    del focusmap[label]
            else:
                if label not in hashmap[label_hash]:
                    hashmap[label_hash].append(label)
                focusmap[label] = op

        result = 0
        for i in hashmap:
            for j in range(len(hashmap[i])):
                result += (i+1) * (j+1) * focusmap[hashmap[i][j]]

        return result
