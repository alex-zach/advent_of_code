from ....challenge_runner import ChallengeBase


class Challenge(ChallengeBase):
    _rock = 1
    _paper = 2
    _scissors = 3

    _winPoints = 6
    _drawPoints = 3
    _losePoints = 0

    _opponentMoveMap = {'A': _rock, 'B': _paper, 'C': _scissors}
    _moveMap = {'X': _rock, 'Y': _paper, 'Z': _scissors}

    _winsAgainst = {_rock: _scissors, _paper: _rock, _scissors: _paper}
    _loseAgainst = {_rock: _paper, _paper: _scissors, _scissors: _rock}

    def __init__(self):
        super().__init__(__file__, ('15', '12'))

    def parse_input(self, lines):
        return [l.split(' ') for l in filter(lambda l: len(l) > 0, [l.strip() for l in lines])]
    
    def _score(self, move, opponent_move):
        if self._loseAgainst[move] == opponent_move:
            return move + self._losePoints
        elif self._winsAgainst[move] == opponent_move:
            return move + self._winPoints
        else:
            return move + self._drawPoints

    def solve1(self, rounds):
        score = 0

        for round in rounds:
            score += self._score(self._moveMap[round[1]], self._opponentMoveMap[round[0]])

        return score

    def solve2(self, rounds):
        score = 0

        for round in rounds:
            opponent_move = self._opponentMoveMap[round[0]]

            if round[1] == 'X':
                move = self._winsAgainst[opponent_move]
            elif round[1] == 'Y':
                move = opponent_move
            elif round[1] == 'Z':
                move = self._loseAgainst[opponent_move]

            score += self._score(move, opponent_move)

        return score
