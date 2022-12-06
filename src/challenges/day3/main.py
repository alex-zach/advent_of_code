from ...challenge_runner import ChallengeBase


class Challenge(ChallengeBase):

    def __init__(self):
        super().__init__(__file__, ('157', '70'))

    def parse_input(self, lines):
        return list(filter(lambda l: len(l) > 0, [l.strip() for l in lines]))

    def _duplicate_item_type(self, comps):
        comp_maps = [dict()]

        for c in [*range(ord('a'), ord('z')+1), *range(ord('A'),ord('Z')+1)]:
            comp_maps[0][chr(c)] = 0

        for c in comps[0]:
            comp_maps[0][c] += 1

        for i in range(1,len(comps)):
            comp_maps.append(dict())
            for c in [*range(ord('a'), ord('z')+1), *range(ord('A'),ord('Z')+1)]:
                comp_maps[i][chr(c)] = 0

            for c in comps[i]:
                comp_maps[i][c] = min(comp_maps[i][c] + 1, comp_maps[i-1][c])
        
        return comp_maps[-1]

    def _priority(self, cnt_map):
        score = 0
        for (key, val) in cnt_map.items():
            if key.islower():
                score += (ord(key) - ord('a') + 1)*min(1, val)
            else:
                score += (ord(key) - ord('A') + 27)*min(1, val)
        return score

    def solve1(self, rucksacks):
        return sum([
            self._priority(self._duplicate_item_type((rucksack[:len(rucksack)//2], rucksack[len(rucksack)//2:]))) \
            for rucksack in rucksacks
        ])

    def solve2(self, rucksacks):
        return sum([
            self._priority(self._duplicate_item_type(group)) \
            for group in [rucksacks[i:i+3] for i in range(0, len(rucksacks), 3)]
        ])
