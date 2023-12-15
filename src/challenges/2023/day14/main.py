from ....challenge_runner import ChallengeBase


class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('136', '64'))
    
    def parse_input(self, lines):
        return [line.strip() for line in lines if len(line.strip()) > 0]

    def solve1(self, grid):
        total_load = 0
        for i in range(len(grid[0])):
            pos = len(grid)
            for j in range(len(grid)):
                if grid[j][i] == 'O':
                    total_load += pos
                    pos -= 1
                elif grid[j][i] == '#':
                    pos = len(grid) - j - 1

        return total_load

    def solve2(self, grid):
        grid = tuple(grid)

        def rot_cw(g):
            return tuple(''.join(g[i][j] for i in reversed(range(len(g)))) for j in range(len(g[0])))

        def tilt_east(g):
            return tuple('#'.join(''.join(sorted(part)) for part in l.split('#')) for l in g)

        def cycle(g):
            for _ in range(4):
                g = tilt_east(rot_cw(g))
            return g

        cyclecnt = 1_000_000_000
        cache = {}
        cache[grid] = 0
        for i in range(1, cyclecnt + 1):
            grid = cycle(grid)
            if grid in cache:
                start = cache[grid]
                length = i - start
                rest = (cyclecnt - start) % length + start
                for cached_grid in cache:
                    if cache[cached_grid] == rest:
                        return sum(cached_grid[i].count('O') * (len(cached_grid) - i) for i in range(len(cached_grid)))
            else:
                cache[grid] = i
        
        return sum(grid[i].count('0') * (len(grid) - i) for i in range(len(grid)))
