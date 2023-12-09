import re

from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('114', '2'))
    
    def parse_input(self, lines):
        return [[int(i) for i in line.strip().split()] for line in lines]

    def solve1(self, sequences):
        result = 0
        for seq in sequences:
            dif_seq = [seq]
            while not all([i == 0 for i in dif_seq[-1]]):
                dif_seq.append([dif_seq[-1][i+1] - dif_seq[-1][i] for i in range(len(dif_seq[-1])-1)])
            dif_seq[-1].append(0)
            for i in range(len(dif_seq)-2, -1, -1):
                dif_seq[i].append(dif_seq[i][-1] + dif_seq[i+1][-1])
            result += dif_seq[0][-1]
        return result

    def solve2(self, sequences):
        result = 0
        for seq in sequences:
            seq.reverse()
            dif_seq = [seq]
            while not all([i == 0 for i in dif_seq[-1]]):
                dif_seq.append([dif_seq[-1][i+1] - dif_seq[-1][i] for i in range(len(dif_seq[-1])-1)])
            dif_seq[-1].append(0)
            for i in range(len(dif_seq)-2, -1, -1):
                dif_seq[i].append(dif_seq[i][-1] + dif_seq[i+1][-1])
            result += dif_seq[0][-1]
        return result
