import re
import numpy as np

from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('35', '46'))
    
    def parse_input(self, lines):
        seeds = list(map(lambda x: int(x), re.match(r'seeds: ((?:\d+\s*)+)', lines[0]).group(1).split()))
        maps = []

        map_from = ''
        map_to = ''
        map_ranges = []
        titlep = re.compile(r'(\w+)-to-(\w+) map:')
        rangep = re.compile(r'(\d+) (\d+) (\d+)')
        for line in lines[1:]:
            line = line.strip()
            if line == '':
                if len(map_ranges) > 0:
                    maps.append({
                        'from': map_from,
                        'to': map_to,
                        'ranges': map_ranges
                    })
                    map_from = ''
                    map_to = ''
                    map_ranges = []
                continue
            m = titlep.fullmatch(line)
            if m:
                map_from = m.group(1)
                map_to = m.group(2)
                continue
            m = rangep.fullmatch(line)
            if m:
                map_ranges.append({
                    'dest': int(m.group(1)),
                    'source': int(m.group(2)),
                    'cnt': int(m.group(3))
                })
                continue
            print(f'Warning: skipping "{line}"')
        if len(map_ranges) > 0:
            maps.append({
                'from': map_from,
                'to': map_to,
                'ranges': map_ranges
            })
        return seeds, maps

    def solve1(self, input):
        seeds, maps = input

        for map in maps:
            for i in range(len(seeds)):
                for r in map['ranges']:
                    if seeds[i] >= r['source'] and seeds[i] < (r['source'] + r['cnt']):
                        seeds[i] = r['dest'] + (seeds[i] - r['source'])
                        break

        return min(seeds)

    def solve2(self, input):
        seeds, maps = input
        seeds = [(seedrange[0], sum(seedrange) - 1) for seedrange in np.array(seeds).reshape((-1,2)).tolist()]

        def intersect(inta, intb):
            if inta[1] < intb[0] or intb[1] < inta[0]:
                return (-1,-1)
            return (max(inta[0], intb[0]), min(inta[1], intb[1]))

        def aWithoutB(inta, intb):
            intersection = intersect(inta, intb)
            if intersection == (-1,-1):
                return inta
            if intersection == inta:
                return (-1, -1)
            if intersection[0] == inta[0]:
                return (intersection[1]+1, inta[1])
            return (inta[0], intersection[0]-1)

        for map in maps:
            new_seeds = []
            for seedrange in seeds:
                for r in map['ranges']:
                    source_int = (r['source'], r['source'] + r['cnt'] - 1)
                    move = r['dest'] - r['source']
                    intersection = intersect(seedrange, source_int)
                    rest = aWithoutB(seedrange, source_int)
                    if intersection != (-1, -1):
                        new_seeds.append((intersection[0] + move, intersection[1] + move))
                    if rest != (-1, -1):
                        seedrange = rest
                    else:
                        break
                else:
                    new_seeds.append(rest)
            seeds = new_seeds
            
        return min([seedrange[0] for seedrange in seeds])
