import re

from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, (13, 30))
    
    def parse_input(self, lines):
        games = {}
        p = re.compile(r'Card\s+(\d+):\s+((?:\d+\s*)*)\|\s+((?:\d+\s*)*)')
        for line in lines:
            m = p.fullmatch(line)
            if not m:
                print(f'Failed parsing line "{line.strip()}"')
            games[m.group(1)] = {
                'winning': [int(i) for i in re.split(r'\s+', m.group(2).strip())],
                'my': [int(i) for i in re.split(r'\s+', m.group(3).strip())],
                'cnt': 1
            }

        return games

    def solve1(self, games):
        points = 0
        for game in games:
            winning = games[game]['winning']
            my = games[game]['my']

            matching = -1
            for nr in my:
                if nr in winning: 
                    matching += 1
            if matching >= 0:
                points += 2**matching

        return points

    def solve2(self, games):
        for game in games:
            winning = games[game]['winning']
            my = games[game]['my']
            cnt = games[game]['cnt']

            matching = 0
            for nr in my:
                if nr in winning: 
                    matching += 1

            while matching > 0:
                games[str(int(game) + matching)]['cnt'] += cnt
                matching -= 1

        total_cnt = 0
        for game in games:
            total_cnt += games[game]['cnt']

        return total_cnt
