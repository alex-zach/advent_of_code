import re

from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ("3", None))
    
    def parse_input(self, lines):
        return [(line[0], int(line[1:])) for line in lines]

    def solve1(self, input):
        freq = 0
        for op, nr in input:
            print(op, nr)
            if op == '+':
                freq += nr
            elif op == '-':
                freq -= nr
            print(freq)
        return freq

    def solve2(self, input):
        return None
