from multiprocessing import Pool
import re

from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('21', '525152'))
    
    def parse_input(self, lines):
        return [
            (springs, list(map(int, arrangement.split(','))))
            for springs, arrangement in \
                [(line.strip().split()) for line in lines if len(line.strip()) > 0]
        ]

    def possible_arrangements(self, el, idx = 0):
        springs, arrangement = el
        if idx == 0:
            self._recursion_memo = {}

        while idx < len(springs) and springs[idx] != '?':
            idx += 1

        all_replaced = idx == len(springs)
        
        cnts = list(map(len, re.findall(r'[^\.]+', springs[0:idx])))
        cs = cnts[0:-1] if springs[idx-1] == '#' and not all_replaced else cnts
        arr = arrangement[0:len(cs)] if not all_replaced else arrangement
        cnts_len = len(cnts)
        if cs != arr or cnts_len > len(arrangement):
            return 0

        if all_replaced:
            return 1

        if cnts_len > 0 and springs[idx - 1] == '#':
            if cnts[-1] != arrangement[cnts_len - 1]:
                return self.possible_arrangements((springs.replace('?', '#', 1), arrangement), idx+1)
            else:
                return self.possible_arrangements((springs.replace('?', '.', 1), arrangement), idx+1)

        if cnts_len > 0 and (idx, cnts_len) in self._recursion_memo:
            return self._recursion_memo[(idx, cnts_len)]

        res = self.possible_arrangements((springs.replace('?', '#', 1), arrangement), idx+1) \
                + self.possible_arrangements((springs.replace('?', '.', 1), arrangement), idx+1)

        if cnts_len > 0 and (idx, cnts_len) not in self._recursion_memo:
            self._recursion_memo[(idx, cnts_len)] = res

        return res


    def solve1(self, rows):
        return sum(map(self.possible_arrangements, rows))

    def solve2(self, rows):
        rows = [('?'.join([springs] * 5), arrangement * 5) for springs, arrangement in rows]

        # with Pool(processes=8) as pool:
        #     return sum(pool.map(self.possible_arrangements, rows))

        return sum(map(self.possible_arrangements, rows))