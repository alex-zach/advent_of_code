from copy import deepcopy
from collections import deque

from numpy import zeros

from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('3', '1623178306'))
    
    def parse_input(self, lines):
        return [int(line.strip()) for line in lines if len(line.strip()) > 0]

    def solve1(self, encrypted):
        unique_encrypted = enumerate(encrypted)
        queue = deque(deepcopy(unique_encrypted))

        for e in unique_encrypted:
            if e[1] == 0:
                continue
            while queue[0] != e:
                queue.rotate(1)

            queue.popleft()
            queue.rotate(-e[1])
            queue.append(e)    
        
        zero = (encrypted.index(0), 0)
        while queue[0] != zero:
            queue.rotate(1)

        return sum(queue[pos % len(queue)][1] for pos in (1000,2000,3000))

    def solve2(self, encrypted):
        encrypted = [e * 811589153 for e in encrypted]
        unique_encrypted = list(enumerate(encrypted))
        queue = deque(unique_encrypted)

        for _ in range(10):
            for e in unique_encrypted:
                if e[1] == 0:
                    continue
                while queue[0] != e:
                    queue.rotate(1)

                queue.popleft()
                queue.rotate(-e[1])
                queue.append(e)    
            
        zero = (encrypted.index(0), 0)
        while queue[0] != zero:
            queue.rotate(1)

        return sum(queue[pos % len(queue)][1] for pos in (1000,2000,3000))