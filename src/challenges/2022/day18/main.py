import re
import sys
import os

from ....challenge_runner import ChallengeBase

sys.setrecursionlimit(3000)

def sign(x):
    return 1 if x > 0 else -1 if x < 0 else 0

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('64', '58'))
    
    def parse_input(self, lines):
        p = re.compile(r'(\d+),(\d+),(\d+)')
        cubes = []
        for line in lines:
            m = p.match(line.strip())
            if m:
                cubes.append((int(m.group(1)), int(m.group(2)), int(m.group(3))))
        return cubes

    def solve1(self, cubes):
        def norm1(c1, c2):
            x1,y1,z1 = c1
            x2,y2,z2 = c2

            return abs(x1-x2) + abs(y1-y2) + abs(z1-z2)

        return sum([6 - len([1 for c2 in cubes if norm1(c,c2) == 1]) for c in cubes])

    def solve2(self, cubes):
        def norm1(c1, c2):
            x1,y1,z1 = c1
            x2,y2,z2 = c2

            return abs(x1-x2) + abs(y1-y2) + abs(z1-z2)

        cubes_set = set(cubes)
        xmin, xmax = min(map(lambda x: x[0], cubes_set)), max(map(lambda x: x[0], cubes_set))
        ymin, ymax = min(map(lambda x: x[1], cubes_set)), max(map(lambda x: x[1], cubes_set))
        zmin, zmax = min(map(lambda x: x[2], cubes_set)), max(map(lambda x: x[2], cubes_set))
        
        # all air except the boundaries
        air_set = set()
        for x in range(xmin-1, xmax, 1):
            for y in range(ymin-1, ymax, 1):
                for z in range(zmin-1, zmax, 1):
                    if (x,y,z) not in cubes_set:
                        air_set.add((x,y,z))

        # remove all air next to removed air
        for dist in range(1, max(xmax,ymax,zmax)):
            to_remove = set()
            for x,y,z in air_set:
                if x == xmin + dist or x == xmax - dist or y == ymin + dist or y == ymax - dist or z == zmin + dist or z == zmax - dist:
                    for xd,yd,zd in ((-1,0,0),(1,0,0),(0,-1,0),(0,1,0),(0,0,-1),(0,0,1)):
                        if (x+xd,y+yd,z+zd) not in air_set and (x+xd, y+yd, z+zd) not in cubes_set:
                            to_remove.add((x,y,z))
                            break
            if len(to_remove) == 0:
                break
            else:
                air_set -= to_remove

        # add remaining air to cubes
        cubes_set |= air_set

        return sum([6 - len([1 for c2 in cubes_set if norm1(c,c2) == 1]) for c in cubes_set])
