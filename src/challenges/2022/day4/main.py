import re
from ....challenge_runner import ChallengeBase


class Challenge(ChallengeBase):

    def __init__(self):
        super().__init__(__file__, ('2', '4'))

    def parse_input(self, lines):
        pairs = []

        p = re.compile(r'(\d+)-(\d+),(\d+)-(\d+)')

        for line in lines:
            match = p.match(line)
            if match:
                pairs.append((set(range(int(match.group(1)),int(match.group(2))+1)), set(range(int(match.group(3)),int(match.group(4))+1))))

        return pairs

    def solve1(self, elves):
        return sum([1 if elve[0] <= elve[1] or elve[1] <= elve[0] else 0 for elve in elves])

    def solve2(self, elves):
        return sum([min(len(elve[0].intersection(elve[1])), 1) for elve in elves])
