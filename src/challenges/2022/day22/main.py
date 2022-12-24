import re

from ....challenge_runner import ChallengeBase

def add(a,b):
    return (a[0] + b[0], a[1] + b[1])


class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('6032', None))
    
    def parse_input(self, lines):
        max_width = max(len(line.replace('\n', '')) for line in lines[:-2])
        grid = []

        grid.append('V' * (max_width + 2))
        for line in lines[:-2]:
            line = 'V' + line.replace('\n', '').replace(' ', 'V')
            line += 'V' * (max_width - len(line) + 2)
            grid.append(line)
        grid.append('V' * (max_width + 2))

        instructions = []
        p = re.compile(r'((\d+)|([RL]))')
        instruction = lines[-1]
        while len(instruction) > 0:
            m = p.match(instruction)
            
            if not m:
                break

            if m.group(2) is not None:
                instructions.append(int(m.group(2)))
            else:
                instructions.append(m.group(3))
            
            instruction = instruction[m.end():]

        return grid, instructions

    def solve1(self, input):
        grid, instructions = input
        facings = [(0,1), (1,0), (0,-1), (-1,0)]

        facing = 0
        position = (1, grid[1].index('.'))

        for instr in instructions:
            if type(instr) is int:
                for _ in range(instr):
                    x,y = add(position, facings[facing])
                    if grid[x][y] == 'V':
                        while grid[x][y] == 'V':
                            x,y = add((x,y), facings[facing])
                            x %= len(grid)
                            y %= len(grid[x])
                    if grid[x][y] == '#':
                        break
                    elif grid[x][y] == '.':
                        position = x,y
                        
            elif instr == 'R':
                facing += 1
                facing %= len(facings)
            elif instr == 'L':
                facing -= 1
                facing %= len(facings)
        
        return 1000 * position[0] + 4 * position[1] + facing

    def solve2(self, input):
        return None
