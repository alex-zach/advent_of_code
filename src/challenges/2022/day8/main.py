from functools import reduce
from operator import mul
from ....challenge_runner import ChallengeBase


class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('21', '8'))

    def parse_input(self, lines):
        return [[int(c) for c in line.strip()] for line in filter(lambda line: len(line.strip()) > 0, lines)]
            
    def solve1(self, grid):
        rows = len(grid)
        cols = len(grid[0])

        innercnt = 0

        for row in range(1, rows-1):
            for col in range(1, cols-1):
                for rowrange, colrange in [
                    (range(row+1, rows),(col,)), 
                    ((row,),range(col+1, cols)), 
                    (range(0, row),(col,)), 
                    ((row,), range(0, col))]:

                    max_tree = max([grid[r][c] for c in colrange for r in rowrange])

                    if max_tree < grid[row][col]:
                        innercnt += 1
                        break

        return rows * 2 + (cols-2) * 2 + innercnt

    def solve2(self, grid):
        rows = len(grid)
        cols = len(grid[0])

        max_sceenic_score = 0

        for row in range(1, rows-1):
            for col in range(1, cols-1):
                view_distance = [0, 0, 0, 0]
                for idx, rowdir, coldir in [(0,1,0), (1,-1,0), (2,0,1), (3,0,-1)]:
                    r = row + rowdir
                    c = col + coldir
                    while r < rows and r >= 0 and c < cols and c >= 0:
                        view_distance[idx] += 1

                        if grid[r][c] >= grid[row][col]:
                            break

                        r += rowdir
                        c += coldir
                sceenic_score = reduce(mul, view_distance, 1)
                max_sceenic_score = max(max_sceenic_score, sceenic_score)
                    
        return max_sceenic_score