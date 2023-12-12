import enum
import re

from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('374', '82000210'))
    
    def parse_input(self, lines):
        return [list(line.strip()) for line in lines if len(line.strip()) > 0]

    def solve1(self, grid):
        galaxies = [(i,j) for i in range(len(grid)) for j in range(len(grid[i])) if grid[i][j] == '#']
        galaxy_rows = set([i for i,_ in galaxies])
        galaxy_cols = set([j for _,j in galaxies])

        added_rows = 0
        added_cols = 0
        for i in range(len(grid)):
            if i in galaxy_rows: continue
            for j, (gal_r, gal_c) in enumerate(galaxies):
                if gal_r - added_rows > i:
                    galaxies[j] = (gal_r + 1, gal_c)
            added_rows += 1
        for i in range(len(grid[0])):
            if i in galaxy_cols: continue
            for j, (gal_r, gal_c) in enumerate(galaxies):
                if gal_c - added_cols > i:
                    galaxies[j] = (gal_r, gal_c + 1)
            added_cols += 1

        result = 0
        for i, (a_r, a_c) in enumerate(galaxies):
            for b_r, b_c in galaxies[i+1:]:
                result += abs(a_r - b_r) + abs(a_c - b_c)

        return result

    def solve2(self, grid):
        expand = 1000000
        
        galaxies = [(i,j) for i in range(len(grid)) for j in range(len(grid[i])) if grid[i][j] == '#']
        galaxy_rows = set([i for i,_ in galaxies])
        galaxy_cols = set([j for _,j in galaxies])

        added_rows = 0
        added_cols = 0
        for i in range(len(grid)):
            if i in galaxy_rows: continue
            for j, (gal_r, gal_c) in enumerate(galaxies):
                if gal_r - added_rows > i:
                    galaxies[j] = (gal_r + expand - 1, gal_c)
            added_rows += expand - 1
        for i in range(len(grid[0])):
            if i in galaxy_cols: continue
            for j, (gal_r, gal_c) in enumerate(galaxies):
                if gal_c - added_cols > i:
                    galaxies[j] = (gal_r, gal_c + expand - 1)
            added_cols += expand - 1

        result = 0
        for i, (a_r, a_c) in enumerate(galaxies):
            for b_r, b_c in galaxies[i+1:]:
                result += abs(a_r - b_r) + abs(a_c - b_c)

        return result
