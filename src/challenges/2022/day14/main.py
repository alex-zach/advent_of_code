from math import inf
import re

from ....challenge_runner import ChallengeBase


def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0


class Cave:
    def __init__(self, paths):
        self.grid = {}
        self.max_depth = 0
        for path in paths:
            for i in range(1, len(path)):
                start = path[i-1]
                end = path[i]
                dirx = sign(end[0] - start[0])
                diry = sign(end[1] - start[1])
                cur = start
                while cur != end:
                    self.set(cur, '#')
                    cur = (cur[0] + dirx, cur[1] + diry)
                self.set(cur, '#')
    
    def set(self, pos, type):
        x,y = pos
        if type == '#' and y > self.max_depth:
            self.max_depth = y
        if str(x) not in self.grid:
            self.grid[str(x)] = {}
        self.grid[str(x)][str(y)] = type

    def drop_sand1(self, drop_pos):
        sand_x,sand_y = drop_pos

        while sand_y <= self.max_depth:
            if self.get((sand_x,sand_y+1)) == '.':
                sand_y += 1
            elif self.get((sand_x-1, sand_y+1)) == '.':
                sand_x -= 1
                sand_y += 1
            elif self.get((sand_x+1, sand_y+1)) == '.':
                sand_x += 1
                sand_y += 1
            else:
                self.set((sand_x,sand_y), 'o')
                return True

        return False
    
    def drop_sand2(self, drop_pos):
        sand_x, sand_y = drop_pos

        if self.get((sand_x,  sand_y)) != '.':
            return False

        while sand_y < self.max_depth + 1:
            if self.get((sand_x,sand_y+1)) == '.':
                sand_y += 1
            elif self.get((sand_x-1, sand_y+1)) == '.':
                sand_x -= 1
                sand_y += 1
            elif self.get((sand_x+1, sand_y+1)) == '.':
                sand_x += 1
                sand_y += 1
            else:
                self.set((sand_x,sand_y), 'o')
                return True

        self.set((sand_x, sand_y), 'o')
        return True

    def __str__(self):
        xs = [int(x) for x in self.grid]
        minx = min(xs)
        maxx = max(xs)

        res = ''
        for j in range(0, self.max_depth+3):
            for i in range(minx, maxx+1):
                res += self.get((i,j))
            res += '\n'
        return res

    def get(self, pos):
        x,y = pos
        if str(x) not in self.grid:
            return '.'
        if str(y) not in self.grid[str(x)]:
            return '.'
        return self.grid[str(x)][str(y)]


class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('24', '93'))
    
    def parse_input(self, lines):
        p = re.compile('(\d+),(\d+)')
        paths = []

        for line in lines:
            path = []
            sp = line.split('->')
            for token in sp:
                m = p.match(token.strip())
                if m:
                    path.append((int(m.group(1)), int(m.group(2))))
            paths.append(path)

        return paths

    def solve1(self, paths):
        cave = Cave(paths)

        cnt = 0
        while cave.drop_sand1((500,0)):
            cnt += 1

        return cnt

    def solve2(self, paths):
        cave = Cave(paths)

        cnt = 0
        while cave.drop_sand2((500,0)):
            cnt += 1

        return cnt
