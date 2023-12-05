from dataclasses import replace
import re

from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, 
            (('142', '142'), (None, '281')), 
            tuple(map(lambda x: f'input.eg.{x}', range(1,3))))
    
    def parse_input(self, lines):
        return lines

    def solve1(self, input):
        val = 0
        for line in input:
            digits = []
            for c in line:
                if c.isdigit():
                    digits.append(c)
            if len(digits) > 0:
                val += int(digits[0] + digits[-1])
        return val

    def solve2(self, input):
        rep = {'one': 'o1e', 'two': 't2o', 'three': 't3e', 'four': 'f4r', 'five': 'f5e', 'six': 's6x', 'seven': 's7n', 'eight': 'e8t', 'nine': 'n9e'}
        val = 0
        zeroval = ord('0')
        for line in input:
            for r in rep:
                line = line.replace(r, rep[r])
            for c in line:
                if c.isdigit():
                    val += (ord(c) - zeroval) * 10
                    break
            for c in line[::-1]:
                if c.isdigit():
                    val += ord(c) - zeroval
                    break
        return val

