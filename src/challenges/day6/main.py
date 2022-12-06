from ...challenge_runner import ChallengeBase


class Challenge(ChallengeBase):

    def __init__(self):
        super().__init__(__file__, 
            (('7', '19'), ('5', '23'), ('6', '23'), ('10', '29'), ('11', '26')), 
            tuple(map(lambda x: f'input.eg.{x}', range(1,6))))

    def parse_input(self, lines):
        return list(lines[0])

    def _first_unique_seq(self, seq, length):
        for i in range(len(seq)-length):
            if len(set(seq[i:i+length])) == length:
                return i + length
        
        return -1

    def solve1(self, seq):
        return self._first_unique_seq(seq, 4)


    def solve2(self, seq):
        return self._first_unique_seq(seq, 14)