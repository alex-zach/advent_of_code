from functools import cmp_to_key
import json

from ...challenge_runner import ChallengeBase


class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('13', '140'))

    def parse_input(self, lines):
        packets = []
        for i in range(0, len(lines), 3):
            packets.append((json.loads(lines[i].strip()), json.loads(lines[i+1].strip())))
        return packets
            
    def solve1(self, packets):
        def cmp(left, right):
            for i in range(len(left)):
                if i >= len(right):
                    return False
                if type(left[i]) == list or type(right[i]) == list:
                    new_left = left[i] if type(left[i]) == list else [left[i]]
                    new_right = right[i] if type(right[i]) == list else [right[i]]
                    res = cmp(new_left, new_right)
                    if res is not None:
                        return res
                    else:
                        continue
                if left[i] > right[i]:
                    return False
                if left[i] < right[i]:
                    return True
            if len(left) == len(right):
                return None
            return True

        total = 0
        for idx, (left, right) in enumerate(packets):
            if cmp(left,right):
                total += idx+1
        return total
    
    def solve2(self, packets):
        def cmp(left, right):
            for i in range(len(left)):
                if i >= len(right):
                    return 1
                if type(left[i]) == list or type(right[i]) == list:
                    new_left = left[i] if type(left[i]) == list else [left[i]]
                    new_right = right[i] if type(right[i]) == list else [right[i]]
                    res = cmp(new_left, new_right)
                    if res != 0:
                        return res
                    else:
                        continue
                if left[i] > right[i]:
                    return 1
                if left[i] < right[i]:
                    return -1
            if len(left) == len(right):
                return 0
            return -1

        packets = [pkt for pkts in packets for pkt in pkts ]
        packets.append([[2]])
        packets.append([[6]])
        packets.sort(key=cmp_to_key(cmp))

        return (packets.index([[2]]) + 1) * (packets.index([[6]]) + 1)
        

