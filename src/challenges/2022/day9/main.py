import re

from ....challenge_runner import ChallengeBase


def sign(x):
    return 1 if x > 0 else -1 if x < 1 else 0


class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, 
            (('13', '1'), ('88', '36')),
            tuple(map(lambda x: f'input.eg.{x}', range(1,3)))
        )

    def parse_input(self, lines):
        p = re.compile(r'([RULD]) (\d+)')
        
        moves = []
        for line in lines:
            m = p.match(line)
            if m:
                moves.append((m.group(1), int(m.group(2))))
        
        return moves
            
    def solve1(self, moves):
        return self.solve2(moves, 2)

    
    def solve2(self, moves, rope_len=10):
        rope = [[0,0] for _ in range(rope_len)]
        tail_set = set()
        tail_set.add(tuple(rope[rope_len - 1]))

        for dir, cnt in moves:
            if dir == 'U':
                x_dir, y_dir = 0, 1
            elif dir == 'D':
                x_dir, y_dir = 0, -1
            elif dir == 'R':
                x_dir, y_dir = 1, 0
            else:
                x_dir, y_dir = -1, 0

            for _ in range(cnt):
                rope[0][0] += x_dir
                rope[0][1] += y_dir

                for i in range(1, rope_len):
                    euclid_norm_sq = (rope[i-1][0] - rope[i][0]) ** 2 + (rope[i-1][1] - rope[i][1]) ** 2

                    if euclid_norm_sq >= 4:
                        if rope[i-1][0] - rope[i][0] != 0:
                            rope[i][0] += sign(rope[i-1][0] - rope[i][0])
                        if rope[i-1][1] - rope[i][1] != 0:
                            rope[i][1] += sign(rope[i-1][1] - rope[i][1])

                tail_set.add(tuple(rope[rope_len - 1]))

        return len(tail_set)

