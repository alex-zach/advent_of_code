from copy import deepcopy
from math import comb
import re
from tqdm import tqdm
from ....challenge_runner import ChallengeBase


def piece_gen(pieces):
    piece_cnt = 0
    while True:
        yield pieces[piece_cnt % len(pieces)]
        piece_cnt += 1


def jet_gen(jet_pattern):
    jet_cnt = 0
    while True:
        yield 1 if jet_pattern[jet_cnt % len(jet_pattern)] == '>' else -1
        jet_cnt += 1


class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('3068', '1514285714288'))
    
    def parse_input(self, lines):
        return list(lines[0].strip())

    def solve1(self, jet_pattern):
        pieces = [
            [[True, True, True, True]], 
            [[False, True, False], [True, True, True], [False, True, False]], 
            [[True, True, True], [False, False, True], [False, False, True]],
            [[True], [True], [True], [True]],
            [[True, True], [True, True]]
        ]

        piece = piece_gen(pieces)
        jet = jet_gen(jet_pattern)

        chamber_width = 7
        chamber = []

        for _ in range(2022):
            max_height = len(chamber)
            p = next(piece)
            p_width = len(p[0])
            p_height = len(p)
            bottom_pos = max_height + 3
            left_pos = 2
            for _ in range(3):
                jet_dir = next(jet)
                if left_pos + jet_dir >= 0 and left_pos + p_width + jet_dir <= chamber_width:
                    left_pos += jet_dir
                bottom_pos -= 1

            while True:
                jet_dir = next(jet)

                colission = left_pos + jet_dir < 0 or left_pos + p_width + jet_dir > chamber_width
                if not colission:
                    for h in range(bottom_pos, min(bottom_pos + p_height, max_height), 1):
                        if any([chamber[h][left_pos + jet_dir + i] and p[h-(bottom_pos)][i] for i in range(p_width)]):
                            colission = True
                if not colission:
                    left_pos += jet_dir

                if max_height == 0 and bottom_pos == 0:
                    for h in range(p_height):
                        chamber.append([False if i < left_pos or i > left_pos + p_width - 1 else p[h][i-left_pos] for i in range(7)])
                    break
                
                colission = False
                for h in range(bottom_pos-1, min(bottom_pos + p_height - 1, max_height), 1):
                    if any([chamber[h][left_pos + i] and p[h-(bottom_pos-1)][i] for i in range(p_width)]):
                        colission = True
                
                if colission:
                    for h in range(bottom_pos, bottom_pos + p_height, 1):
                        if h < max_height:
                            for i in range(p_width):
                                chamber[h][left_pos + i] = chamber[h][left_pos + i] or p[h-bottom_pos][i]
                        else:
                            chamber.append([False if i < left_pos or i > left_pos + p_width - 1 else p[h-bottom_pos][i-left_pos] for i in range(7)])
                    break

                bottom_pos -= 1

        # for i in range(len(chamber)-1, -1, -1):
        #     print("".join(['#' if c else '.' for c in chamber[i]]))

        return len(chamber)

    def solve2(self, jet_pattern):
        total = 1000000000000
        pieces = [
            [[True, True, True, True]], 
            [[False, True, False], [True, True, True], [False, True, False]], 
            [[True, True, True], [False, False, True], [False, False, True]],
            [[True], [True], [True], [True]],
            [[True, True], [True, True]]
        ]            

        chamber_width = 7
        chamber = []

        piece_cnt = 0
        jet_cnt = 0
        cnt = 0
        jet_pos = {}
        chambers = {}
        while cnt < total:
            max_height = len(chamber)
            p = pieces[piece_cnt % len(pieces)]
            piece_cnt += 1
            p_width = len(p[0])
            p_height = len(p)
            bottom_pos = max_height + 3
            left_pos = 2
            for _ in range(3):
                jet_dir = 1 if jet_pattern[jet_cnt % len(jet_pattern)] == '>' else -1
                jet_cnt += 1
                if left_pos + jet_dir >= 0 and left_pos + p_width + jet_dir <= chamber_width:
                    left_pos += jet_dir
                bottom_pos -= 1

            while True:
                jet_dir = 1 if jet_pattern[jet_cnt % len(jet_pattern)] == '>' else -1
                jet_cnt += 1

                colission = left_pos + jet_dir < 0 or left_pos + p_width + jet_dir > chamber_width
                if not colission:
                    for h in range(bottom_pos, min(bottom_pos + p_height, max_height), 1):
                        if any([chamber[h][left_pos + jet_dir + i] and p[h-(bottom_pos)][i] for i in range(p_width)]):
                            colission = True
                if not colission:
                    left_pos += jet_dir

                if max_height == 0 and bottom_pos == 0:
                    for h in range(p_height):
                        chamber.append([False if i < left_pos or i > left_pos + p_width - 1 else p[h][i-left_pos] for i in range(7)])
                    break
                
                colission = False
                for h in range(bottom_pos-1, min(bottom_pos + p_height - 1, max_height), 1):
                    if any([chamber[h][left_pos + i] and p[h-(bottom_pos-1)][i] for i in range(p_width)]):
                        colission = True
                
                if colission:
                    for h in range(bottom_pos, bottom_pos + p_height, 1):
                        if h < max_height:
                            for i in range(p_width):
                                chamber[h][left_pos + i] = chamber[h][left_pos + i] or p[h-bottom_pos][i]
                        else:
                            chamber.append([False if i < left_pos or i > left_pos + p_width - 1 else p[h-bottom_pos][i-left_pos] for i in range(7)])
                    break
                
                bottom_pos -= 1
            if piece_cnt % len(pieces) == 0:
                chambers[cnt] = deepcopy(chamber)
                if jet_cnt % len(jet_pattern) in jet_pos:
                    break
                jet_pos[jet_cnt % len(jet_pattern)] = cnt
            cnt += 1

        # print(chambers[cnt])
        # print(chambers[jet_pos[jet_cnt % len(jet_pattern)]])
        
        # for i in range(len(chambers[cnt])-1, -1, -1):
        #     print("%-4d | " % i + "".join(['#' if c else '.' for c in chambers[cnt][i]]))
        # print()
        # for i in range(len(chambers[jet_pos[jet_cnt % len(jet_pattern)]])-1, -1, -1):
        #     print("%-4d | " % i + "".join(['#' if c else '.' for c in chambers[jet_pos[jet_cnt % len(jet_pattern)]][i]]))

        start = len(chambers[jet_pos[jet_cnt % len(jet_pattern)]])
        repeat_part = chambers[cnt][start:]
        iterations = cnt - jet_pos[jet_cnt % len(jet_pattern)]

        # for i in range(len(repeat_part)-1, -1, -1):
        #     print("%-4d | " % i + "".join(['#' if c else '.' for c in repeat_part[i]]))
        it_cnt = (total - cnt) // iterations
        cnt += it_cnt * iterations + 1

        while cnt < total:
            max_height = len(chamber)
            p = pieces[piece_cnt % len(pieces)]
            piece_cnt += 1
            p_width = len(p[0])
            p_height = len(p)
            bottom_pos = max_height + 3
            left_pos = 2
            for _ in range(3):
                jet_dir = 1 if jet_pattern[jet_cnt % len(jet_pattern)] == '>' else -1
                jet_cnt += 1
                if left_pos + jet_dir >= 0 and left_pos + p_width + jet_dir <= chamber_width:
                    left_pos += jet_dir
                bottom_pos -= 1

            while True:
                jet_dir = 1 if jet_pattern[jet_cnt % len(jet_pattern)] == '>' else -1
                jet_cnt += 1

                colission = left_pos + jet_dir < 0 or left_pos + p_width + jet_dir > chamber_width
                if not colission:
                    for h in range(bottom_pos, min(bottom_pos + p_height, max_height), 1):
                        if any([chamber[h][left_pos + jet_dir + i] and p[h-(bottom_pos)][i] for i in range(p_width)]):
                            colission = True
                if not colission:
                    left_pos += jet_dir

                if max_height == 0 and bottom_pos == 0:
                    for h in range(p_height):
                        chamber.append([False if i < left_pos or i > left_pos + p_width - 1 else p[h][i-left_pos] for i in range(7)])
                    break
                
                colission = False
                for h in range(bottom_pos-1, min(bottom_pos + p_height - 1, max_height), 1):
                    if any([chamber[h][left_pos + i] and p[h-(bottom_pos-1)][i] for i in range(p_width)]):
                        colission = True
                
                if colission:
                    for h in range(bottom_pos, bottom_pos + p_height, 1):
                        if h < max_height:
                            for i in range(p_width):
                                chamber[h][left_pos + i] = chamber[h][left_pos + i] or p[h-bottom_pos][i]
                        else:
                            chamber.append([False if i < left_pos or i > left_pos + p_width - 1 else p[h-bottom_pos][i-left_pos] for i in range(7)])
                    break
                
                bottom_pos -= 1
            cnt += 1


        return len(chamber) + it_cnt * len(repeat_part)
