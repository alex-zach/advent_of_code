import re

from concurrent.futures import ThreadPoolExecutor
from ....challenge_runner import ChallengeBase, is_eg_param

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('26', '56000011'))
    
    def parse_input(self, lines):
        p = re.compile(r'Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')

        sensors = []
        for line in lines:
            m = p.match(line)
            if m:
                sensors.append((
                    (int(m.group(1)), int(m.group(2))),
                    (int(m.group(3)), int(m.group(4)))
                ))

        return sensors

    @is_eg_param
    def solve1(self, sensors, eg=False):
        target_y = 10 if eg else 2000000

        beacons_x = set([s[1][0] for s in sensors if s[1][1] == target_y])
        blocked = set()

        for s in sensors:
            (sx, sy), (bx, by) = s
            dist = abs(sx-bx) + abs(sy-by)
            target_dist = abs(sy-target_y)
            for i in range(-(dist-target_dist), dist-target_dist+1, 1):
                blocked.add(sx+i)

        blocked -= beacons_x

        return len(blocked)

    @is_eg_param
    def solve2(self, sensors, eg=False):
        min_xy = 0
        max_xy = 20 if eg else 4000000

        def mapfunc(s):
            (sx,sy),(bx,by)=s
            return (sx,sy), abs(sx-bx) + abs(sy-by)
        
        # sort largest ball to smallest
        sensors = list(sorted(map(mapfunc, sensors), key=lambda x: x[1], reverse=True))

        # remove subsets of other balls
        i = 0
        while i < len(sensors):
            (sx,sy), dist = sensors[i]
            delete = False
            for j in range(i):
                (s2x, s2y), dist2 = sensors[j]
                if abs(s2x-sx) + abs(s2y-sy) + dist <= dist2:
                    delete = True
                    break
            if delete:
                sensors.pop(i)
            else:
                i+=1
        
        # check line if there is a free spot
        def checkline(target_y):
            x_blocked = []
            for s in sensors:
                (sx, sy), dist = s
                target_dist = abs(sy-target_y)
                if target_dist <= dist:
                    x_blocked.append((sx-(dist-target_dist), sx+(dist-target_dist)))

            i = min_xy
            while i <= max_xy:
                for minx, maxx in x_blocked:
                    if i >= minx and i <= maxx:
                        i = maxx + 1
                        break
                else:
                    return i, target_y
            return None


        f = filter(lambda x: x is not None, map(checkline, range(min_xy, max_xy+1)))
        x,y = next(f)
        return x * 4000000 + y