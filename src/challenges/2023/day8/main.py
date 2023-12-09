import re
import numpy as np

from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, 
            (('2', '2'), ('6', '6'), (None, '6')), 
            tuple(map(lambda x: f'input.eg.{x}', range(1,4))))
    
    def parse_input(self, lines):
        instructions = [0 if c == 'L' else 1 for c in lines[0].strip()]

        nodes = {}
        p = re.compile(r'([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)')
        for line in lines[2:]:
            m = p.fullmatch(line.strip())
            if m:
                nodes[m.group(1)] = [m.group(2), m.group(3)]
            else:
                print(f'Warning skipping: {line}')

        return instructions, nodes

    def solve1(self, input):
        instructions, nodes = input
        current = 'AAA'
        i = 0
        while current != 'ZZZ':
            current = nodes[current][instructions[i % len(instructions)]]
            i+= 1

        return i

    def solve2(self, input):
        instructions, nodes = input
        
        start_nodes = list(filter(lambda x: x[2] == 'A', nodes))
        cycle_len = []

        for current in start_nodes:
            j = 0
            while current[2] != 'Z':
                current = nodes[current][instructions[j % len(instructions)]]
                j += 1
            cycle_len.append(j)
        
        return np.lcm.reduce(cycle_len)
