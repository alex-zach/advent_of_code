import re

from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('46', '51'))
    
    def parse_input(self, lines):
        return [line.strip() for line in lines if len(line.strip()) > 0]

    def solve1(self, grid):
        def simulate_beam(pos, dir, total_visited: set):
            while (pos, dir) not in total_visited and pos[0] >= 0 and pos[0] < len(grid) and pos[1] >= 0 and pos[1] < len(grid[0]):
                total_visited.add((pos,dir))
                cur = grid[pos[0]][pos[1]]
                if cur in '/\\':
                    fac = 1 if cur == '/' else -1
                    if dir == (0, 1):
                        dir = (fac * -1, 0)
                    elif dir == (0, -1):
                        dir = (fac * 1, 0)
                    elif dir == (1, 0):
                        dir = (0, fac * -1)
                    else:
                        dir = (0, fac * 1)
                elif cur == '|' and dir[1] != 0:
                    return simulate_beam(pos,(1,0), simulate_beam(pos,(-1,0), total_visited))
                elif cur == '-' and dir[0] != 0:
                    return simulate_beam(pos,(0,1), simulate_beam(pos,(0,-1), total_visited))
                
                pos = (pos[0] + dir[0], pos[1] + dir[1])

            return total_visited

        return len(set(map(lambda x: x[0], simulate_beam((0,0),(0,1), set()))))

    def solve2(self, grid):
        def simulate_beam(pos, dir, total_visited: set):
            while (pos, dir) not in total_visited and pos[0] >= 0 and pos[0] < len(grid) and pos[1] >= 0 and pos[1] < len(grid[0]):
                total_visited.add((pos,dir))
                cur = grid[pos[0]][pos[1]]
                if cur in '/\\':
                    fac = 1 if cur == '/' else -1
                    if dir == (0, 1):
                        dir = (fac * -1, 0)
                    elif dir == (0, -1):
                        dir = (fac * 1, 0)
                    elif dir == (1, 0):
                        dir = (0, fac * -1)
                    else:
                        dir = (0, fac * 1)
                elif cur == '|' and dir[1] != 0:
                    return simulate_beam(pos,(1,0), simulate_beam(pos,(-1,0), total_visited))
                elif cur == '-' and dir[0] != 0:
                    return simulate_beam(pos,(0,1), simulate_beam(pos,(0,-1), total_visited))
                
                pos = (pos[0] + dir[0], pos[1] + dir[1])

            return total_visited

        energized = []
        for i in range(len(grid)):
            energized.append(len(set(map(lambda x: x[0], simulate_beam((i,0),(0,1), set())))))
            energized.append(len(set(map(lambda x: x[0], simulate_beam((i,len(grid[i])-1),(0,-1), set())))))
        for j in range(len(grid[0])):
            energized.append(len(set(map(lambda x: x[0], simulate_beam((0,j),(1,0), set())))))
            energized.append(len(set(map(lambda x: x[0], simulate_beam((len(grid)-1,j),(-1,0), set())))))

        return max(energized)
