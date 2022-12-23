import re

from itertools import product
from ....challenge_runner import ChallengeBase


def add(a,b):
    return (a[0] + b[0], a[1] + b[1])


class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, 
            (('25', '4'), ('110', '20')), 
            tuple(map(lambda x: f'input.eg.{x}', range(1,3))))
    
    def parse_input(self, lines):
        elves = []

        for x, line in enumerate(lines):
            for y, c in enumerate(line):
                if c == '#':
                    elves.append((x,y))

        return set(elves)

    def solve1(self, elves):
        directions = [(-1,0), (1,0), (0,-1), (0,1)]

        for i in range(10):
            proposed_pos = {}

            for elve in elves:
                if all(add(elve, c) not in elves for c in product(range(-1,2,1), range(-1,2,1)) if not c[0] == c[1] == 0):
                    continue # elve doesn't move
                
                for dir_idx in range(len(directions)):
                    dir = directions[(i + dir_idx) % len(directions)]

                    check = [dir]
                    if dir[0] == 0:
                        check.append((-1, dir[1]))
                        check.append((1, dir[1]))
                    else:
                        check.append((dir[0], -1))
                        check.append((dir[0], 1))

                    #print([add(elve, c) for c in check])
                    if all(add(elve, c) not in elves for c in check):
                        proposed_pos[elve] = add(elve, dir)
                        break
            
            goals = {}
            for k, v in proposed_pos.items():
                if v not in goals:
                    goals[v] = [k]
                else:
                    goals[v].append(k)
            
            for v in goals:
                if len(goals[v]) > 1:
                    for k in goals[v]:
                        del proposed_pos[k]
            
            for k in proposed_pos:
                elves.remove(k)
                elves.add(proposed_pos[k])

        x = [e[0] for e in elves]
        y = [e[1] for e in elves]

        return (max(x) - min(x) + 1) * (max(y) - min(y) + 1) - len(elves)

    def solve2(self, elves):
        directions = [(-1,0), (1,0), (0,-1), (0,1)]
        cnt = 0

        while True:
            proposed_pos = {}

            for elve in elves:
                if all(add(elve, c) not in elves for c in product(range(-1,2,1), range(-1,2,1)) if not c[0] == c[1] == 0):
                    continue # elve doesn't move
                
                for dir_idx in range(len(directions)):
                    dir = directions[(cnt + dir_idx) % len(directions)]

                    check = [dir]
                    if dir[0] == 0:
                        check.append((-1, dir[1]))
                        check.append((1, dir[1]))
                    else:
                        check.append((dir[0], -1))
                        check.append((dir[0], 1))

                    #print([add(elve, c) for c in check])
                    if all(add(elve, c) not in elves for c in check):
                        proposed_pos[elve] = add(elve, dir)
                        break
            
            goals = {}
            for k, v in proposed_pos.items():
                if v not in goals:
                    goals[v] = [k]
                else:
                    goals[v].append(k)
            
            for v in goals:
                if len(goals[v]) > 1:
                    for k in goals[v]:
                        del proposed_pos[k]
            
            moved = False
            for k in proposed_pos:
                elves.remove(k)
                elves.add(proposed_pos[k])
                moved = True
            
            cnt += 1

            if not moved:
                break

        return cnt
