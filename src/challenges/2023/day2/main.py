import re

from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('8', '2286'))
    
    def parse_input(self, lines):
        games = {}
        
        p = re.compile(r'Game (\d+):((?:\s*\d+\s+\w+,?;?)+)')
        for line in lines:
            m = p.fullmatch(line.strip())
            if not m:
                print(f'Error {line}')
                continue

            raw_rounds = [t.strip() for t in m.group(2).split(';')]
            rounds = []
            for raw_round in raw_rounds:
                raw_draws = [t.strip() for t in raw_round.split(',')]
                draws = [raw_draw.split(' ') for raw_draw in raw_draws]
                draws = [(int(a), b) for (a,b) in draws]
                rounds.append(draws)
            
            games[m.group(1)] = rounds

        return games

    def solve1(self, games):
        sum = 0
        possible_cnt = {'red': 12, 'green': 13, 'blue': 14}
        for g in games:
            possible = True
            for round in games[g]:
                if not possible: break
                for (cnt, color) in round:
                    if cnt > possible_cnt[color]:
                        possible = False
                        break
            if possible:
                sum += int(g)
            
        return sum

    def solve2(self, games):
        sum = 0
        
        for g in games:
            max_cnt = {'red': 0, 'green': 0, 'blue': 0}
            for round in games[g]:
                for (cnt, color) in round:
                    if cnt > max_cnt[color]:
                        max_cnt[color] = cnt
            sum += max_cnt['red'] * max_cnt['green'] * max_cnt['blue']
            
        return sum
