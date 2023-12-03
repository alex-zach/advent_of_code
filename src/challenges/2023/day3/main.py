import re

from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('4361', '467835'))
    
    def parse_input(self, lines):
        return lines

    def solve1(self, lines):
        result = 0

        def has_adj_symbol(lines, i, j, directions):
            for i_dir, j_dir in directions:
                if 0 <= i_dir + i and i_dir + i < len(lines) and 0 <= j_dir + j and j_dir + j < len(lines[i_dir + i]):
                    c = lines[i_dir + i][j_dir + j]
                    if c != "." and not c.isdigit():
                        return True
            return False
        
        for line_idx, line in enumerate(lines):
            line = line.strip()
            i = 0
            curnum = 0
            adj = False
            while i < len(line):
                if line[i].isdigit():
                    if curnum == 0:
                        adj = adj or has_adj_symbol(lines, line_idx, i, [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0)])
                    else: 
                        adj = adj or has_adj_symbol(lines, line_idx, i, [(-1,0),(1,0)])
                    curnum = curnum * 10 + (ord(line[i]) - ord('0'))

                elif curnum != 0:
                    adj = adj or has_adj_symbol(lines, line_idx, i, [(1,0),(0,0),(-1,0)])
                    if adj:
                        result += curnum
                    curnum = 0
                    adj = False
                i+=1

            if curnum != 0 and adj:
                result += curnum
            
        return result

    def solve2(self, lines):
        result = 0
        gears_dict = {}

        def find_adj_gears(lines, i, j, directions):
            gears = []
            for i_dir, j_dir in directions:
                if 0 <= i_dir + i and i_dir + i < len(lines) and 0 <= j_dir + j and j_dir + j < len(lines[i_dir + i]):
                    c = lines[i_dir + i][j_dir + j]
                    if c == '*':
                        gears.append((i_dir + i, j_dir + j))
            return gears
        
        for line_idx, line in enumerate(lines):
            line = line.strip()
            i = 0
            curnum = 0
            adj_gears = []
            while i < len(line):
                if line[i].isdigit():
                    if curnum == 0:
                        adj_gears += find_adj_gears(lines, line_idx, i, [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0)])
                    else: 
                        adj_gears += find_adj_gears(lines, line_idx, i, [(-1,0),(1,0)])
                    curnum = curnum * 10 + (ord(line[i]) - ord('0'))

                elif curnum != 0:
                    adj_gears += find_adj_gears(lines, line_idx, i, [(1,0),(0,0),(-1,0)])
                    for gear in adj_gears:
                        if gear not in gears_dict:
                            gears_dict[gear] = []
                        gears_dict[gear].append(curnum)

                    curnum = 0
                    adj_gears = []
                i+=1

            if curnum != 0:
                for gear in adj_gears:
                    if gear not in gears_dict:
                        gears_dict[gear] = []
                    gears_dict[gear].append(curnum)
                adj_gears = []

        for gear in gears_dict:
            if len(gears_dict[gear]) == 2:
                result += gears_dict[gear][0] * gears_dict[gear][1]
            
        return result
