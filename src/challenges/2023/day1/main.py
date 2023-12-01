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
        possible_digits = ['one','two','three','four','five','six','seven','eight','nine']
        val = 0
        for line in input:
            digits = []
            for i, c in enumerate(line):
                if c.isdigit():
                    digits.append(int(c))
                for j, dig in enumerate(possible_digits):
                    if c == dig[0] and line[i:i+len(dig)] == dig:
                        digits.append(j+1)

            val += digits[0] * 10 + digits[-1]

        return val

