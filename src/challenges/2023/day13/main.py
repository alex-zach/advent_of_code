import re

from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('405', '400'))
    
    def parse_input(self, lines):
        grids = [[]]
        for line in lines:
            line = line.strip()
            if len(line) > 0:
                grids[-1].append(line)
            else:
                grids.append([])
        if len(grids[-1]) == 0:
            grids = grids[0:-1]
        return grids

    def solve1(self, grids):
        result = 0
        for grid in grids:
            inverted_grid = [''.join([s[i] for s in grid]) for i in range(len(grid[0]))]
            
            for working_grid, factor in ((grid, 100), (inverted_grid, 1)):
                for i in range(len(working_grid) - 1, 0, -1):
                    cnt = 0
                    while i - cnt > cnt and working_grid[i-cnt] == working_grid[cnt]:
                        cnt += 1
                    if i-cnt < cnt:
                        result += cnt*factor
                        break
                else:
                    for i in range(len(working_grid) - 1):
                        cnt = 0
                        while i + cnt < len(working_grid) - 1 - cnt and working_grid[i + cnt] == working_grid[- 1 - cnt]:
                            cnt += 1
                        if i + cnt > len(working_grid) - 1 - cnt:
                            result += (i + cnt)*factor
                            break
                    else:
                        continue
                break
            
        return result

    def solve2(self, grids):
        result = 0
        for grid in grids:
            inverted_grid = [''.join([s[i] for s in grid]) for i in range(len(grid[0]))]

            def differ_cnt(s1, s2):
                cnt = 0
                for i in range(len(s1)):
                    if s1[i] != s2[i]:
                        cnt += 1
                    if cnt > 1:
                        break
                return cnt
            
            for working_grid, factor in ((grid, 100), (inverted_grid, 1)):
                for i in range(len(working_grid) - 1, 0, -1):
                    cnt = 0
                    dif_cnt = 0
                    while i - cnt > cnt and (cur_dif_cnt := differ_cnt(working_grid[i-cnt], working_grid[cnt])) < 2 and dif_cnt < 2:
                        cnt += 1
                        dif_cnt += cur_dif_cnt
                    if i-cnt < cnt and dif_cnt == 1:
                        result += cnt*factor
                        break
                else:
                    for i in range(len(working_grid) - 1):
                        cnt = 0
                        dif_cnt = 0
                        while i + cnt < len(working_grid) - 1 - cnt and \
                            (cur_dif_cnt := differ_cnt(working_grid[i + cnt],working_grid[- 1 - cnt])) < 2 and \
                                dif_cnt < 2:
                            cnt += 1
                            dif_cnt += cur_dif_cnt
                        if i + cnt > len(working_grid) - 1 - cnt and dif_cnt == 1:
                            result += (i + cnt)*factor
                            break
                    else:
                        continue
                break
            
        return result
