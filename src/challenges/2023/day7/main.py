import functools
import re

from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('6440', '5905'), cached_solutions=(248836197, 251195607))
        
    def parse_input(self, lines):
        hand_bid = []
        rep_dict = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10}
        for line in lines:
            hand,bid = line.strip().split()
            hand = list(hand)
            for i in range(len(hand)):
                if hand[i].isdigit():
                    hand[i] = int(hand[i])
                else:
                    hand[i] = rep_dict[hand[i]]
            hand_bid.append((hand, int(bid)))
        return hand_bid

    # high_card = 0, one_pair = 1, two_pair = 2, three_of_a_kind = 3, full_house = 4, four_of_a_kind = 5, five_of_a_kind = 6
    def get_hand_score(self, hand):
        hand_set_len = len(set(hand))
        if hand_set_len == 5:
            return 0
        if hand_set_len == 4:
            return 1
        if hand_set_len == 3:
            cnt = [0] * 13
            for c in hand:
                cnt[c-2] += 1
            if max(cnt) == 2:
                return 2
            else:
                return 3
        if hand_set_len == 2:
            cnt = [0] * 13
            for c in hand:
                cnt[c-2] += 1
            if max(cnt) == 3:
                return 4
            else:
                return 5
        return 6

    def get_hand_score_with_jokers(self,hand):
        hands = list(map(lambda c: [c] if c != 1 else list(range(2,11))+list(range(12,15)), hand))
        max_score = 0
        for c1 in hands[0]:
            for c2 in hands[1]:
                for c3 in hands[2]:
                    for c4 in hands[3]: 
                        for c5 in hands[4]:
                            cur_hand = [c1, c2, c3, c4, c5]
                            max_score = max(max_score, self.get_hand_score(cur_hand))
        return max_score

    def comp_func(self, el1, el2):
        hand1,score1,_ = el1
        hand2,score2,_ = el2

        if score1 != score2:
            return score1 - score2
        for c1, c2 in zip(hand1, hand2):
            if c1 != c2:
                return c1 - c2
        return 0

    def solve1(self, hand_bid):
        hand_bid = [(hand, self.get_hand_score(hand), bid) for hand,bid in hand_bid]
        hand_bid.sort(key=functools.cmp_to_key(self.comp_func))

        score = 0
        for i, (_,_,bid) in enumerate(hand_bid):
            score += (i+1) * bid

        return score

    def solve2(self, hand_bid):
        hand_bid = [([e if e != 11 else 1 for e in hand], bid) for hand,bid in hand_bid]
        hand_bid = [(hand, self.get_hand_score_with_jokers(hand), bid) for hand,bid in hand_bid]

        hand_bid.sort(key=functools.cmp_to_key(self.comp_func))

        score = 0
        for i, (_,_,bid) in enumerate(hand_bid):
            score += (i+1) * bid

        return score
