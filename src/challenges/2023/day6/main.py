from math import ceil, floor, sqrt
import re

from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('288', '71503'))
    
    def parse_input(self, lines):
        times = map(int, re.split('\s+', lines[0].strip())[1:])
        records = map(int, re.split('\s+', lines[1].strip())[1:])
        return list(zip(times,records))

    def solve1(self, races):
        res = 1
        # distance = x * (time - x) = -x^2 + x * time > record <=> x^2 - x * time < -record <=> x zwischen time/2 +- sqrt(time^2/4 - record)
        for race in races:
            time, record = race
            root = sqrt(time**2/4-record)
            lower_bound = floor(time/2 - root) + 1
            upper_bound = ceil(time/2 + root) - 1

            res *= (upper_bound-lower_bound+1)
        return res

    def solve2(self, races):
        time, record = "", ""
        for race in races:
            time += str(race[0])
            record += str(race[1])

        # distance = x * (time - x) = -x^2 + x * time > record <=> x^2 - x * time < -record <=> x zwischen time/2 +- sqrt(time^2/4 - record)
        time, record = int(time), int(record)
        root = sqrt(time**2/4-record)
        lower_bound = floor(time/2 - root) + 1
        upper_bound = ceil(time/2 + root) - 1

        return upper_bound-lower_bound+1
