import copy
import re
from ...challenge_runner import ChallengeBase


class Challenge(ChallengeBase):

    def __init__(self):
        super().__init__(__file__, ('CMZ', 'MCD'))

    def parse_input(self, lines):
        stacks = []
    
        for i in range(len(lines[0])//4):
            stacks.append([])
        
        lidx = 0
        while lines[lidx][1] != '1':
            for i in range(1, len(stacks)*4, 4):
                if len(lines[lidx][i].strip()) > 0:
                    stacks[(i-1)//4].append(lines[lidx][i])
            lidx += 1
        lidx += 2

        moves = []
        movespattern = re.compile(r'move (\d+) from (\d+) to (\d+)')

        for line in lines[lidx:]:
            match = movespattern.match(line)
            if match:
               moves.append({'move': int(match.group(1)), 'from': int(match.group(2)), 'to': int(match.group(3))})

        return stacks, moves

    def solve1(self, input):
        stacks, moves = copy.deepcopy(input)

        for move in moves:
            for i in range(move['move']):
                stacks[move['to']-1].insert(0, stacks[move['from']-1].pop(0))

        return "".join([s[0] for s in stacks])

    def solve2(self, input):
        stacks, moves = copy.deepcopy(input)

        for move in moves:
            stacks[move['to']-1] = stacks[move['from']-1][0:move['move']] + stacks[move['to']-1]
            stacks[move['from']-1] = stacks[move['from']-1][move['move']:]

        return "".join([s[0] for s in stacks])