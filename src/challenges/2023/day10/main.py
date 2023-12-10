from queue import Queue
import re

from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__,
            (('4', None), ('8', None), (None, '4'), (None, '4'), (None, '8'), (None, '10')), 
            tuple(map(lambda x: f'input.eg.{x}', range(1,7))))
    
    def parse_input(self, lines):
        grid = [list(line.strip()) for line in lines]
        sl, sc = -1,-1
        for i, line in enumerate(grid):
            for j, c in enumerate(line):
                if c == "S":
                    sl, sc = i, j
                    break
            if sl != -1:
                break
        
        north = grid[sl-1][sc] in '|7F' if sl > 0 else False
        south = grid[sl+1][sc] in '|LJ' if sl < len(grid) - 1 else False
        west = grid[sl][sc-1] in '-LF' if sc > 0 else False
        east = grid[sl][sc+1] in '-J7' if sc < len(grid[sl]) - 1 else False

        if north and south: grid[sl][sc] = '|'
        elif north and west: grid[sl][sc] = 'J'
        elif north and east: grid[sl][sc] = 'L'
        elif south and west: grid[sl][sc] = '7'
        elif south and east: grid[sl][sc] = 'F'
        elif west and east: grid[sl][sc] = '-'
        else: 
            print('Error no loop!')
            return -1
        return grid, sl, sc

    def solve1(self, input):
        grid, sl, sc = input

        q = Queue()
        d = {}

        q.put((sl, sc))
        d[(sl, sc)] = 0

        while q.qsize() != 0:
            v = q.get()
            i,j = v
            c = grid[i][j]
            neighbors = []
            if i > 0 and c in '|LJ': neighbors.append((i-1,j))
            if i < len(grid) - 1 and c in '|7F': neighbors.append((i+1,j))
            if j > 0 and c in '-J7': neighbors.append((i,j-1))
            if j < len(grid[i]) - 1 and c in '-LF': neighbors.append((i,j+1))
            for n in neighbors:
                if n in d:
                    continue
                d[n] = d[v] + 1
                q.put(n)
        
        return max(d.values())

    def solve2(self, input):
        grid, sl, sc = input
        
        dir = ''
        if sl > 0 and grid[sl][sc] in '|LJ': dir = 'n'
        elif sl < len(grid) - 1 and grid[sl][sc] in '|7F': dir = 's'
        elif sc > 0 and grid[sl][sc] in '-J7': dir = 'w'
        elif sc < len(grid[sl]) - 1 and grid[sl][sc] in '-LF': dir = 'e'

        loop = [(sl,sc)]

        while len(loop) == 1 or loop[-1] != (sl,sc):
            i,j = loop[-1]
            last_dir = dir
            dir = ''
            if i > 0 and grid[i][j] in '|LJ' and last_dir != 's': dir = 'n'
            elif i < len(grid) - 1 and grid[i][j] in '|7F' and last_dir != 'n': dir = 's'
            elif j > 0 and grid[i][j] in '-J7' and last_dir != 'e': dir = 'w'
            elif j < len(grid[i]) - 1 and grid[i][j] in '-LF' and last_dir != 'w': dir = 'e'
            else:
                print("error")
                return -1
            loop.append((i + (-1 if dir == 'n' else 1 if dir == 's' else 0), j + (-1 if dir == 'w' else 1 if dir == 'e' else 0)))
        
        doubled_grid = [['.' for _ in range(len(grid[0])*2 + 1)] for i in range(len(grid)*2 + 1)]

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if (i,j) not in loop:
                    grid[i][j] = '.'
        for i in range(len(doubled_grid)):
            for j in range(len(doubled_grid[i])):
                if i % 2 == 1 and j % 2 == 1:
                    doubled_grid[i][j] = grid[i//2][j//2]
                elif i % 2 == 0 and j % 2 == 1 and grid[i//2-1][j//2] in '|F7' and grid[i//2][j//2] in '|LJ':
                    doubled_grid[i][j] = '|'
                elif i % 2 == 1 and j % 2 == 0 and grid[i//2][j//2-1] in '-FL' and grid[i//2][j//2] in '-7J':
                    doubled_grid[i][j] = '-'
        
        q = Queue()
        q.put((0,0))
        while q.qsize() != 0:
            i,j = q.get()
            doubled_grid[i][j] = '0'
            for di, dj in ((-1,0),(1,0),(0,-1),(0,1)):
                if i+di >= 0 and i+di < len(doubled_grid) and j+dj >= 0 and j+dj < len(doubled_grid[i+di]) and doubled_grid[i+di][j+dj] == '.':
                    q.put((i+di,j+dj))
                    doubled_grid[i+di][j+dj] = '0'

        cnt = 0
        for i, line in enumerate(doubled_grid):
            for j, c in enumerate(line):
                if i % 2 == 1 and j % 2 == 1 and c == '.':
                    cnt += 1

        return cnt
