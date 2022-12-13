from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('24000', '45000'))

    def parse_input(self, lines):
        calories = []
        calorie_count = 0
        for line in lines:
            if len(line.strip()) > 0:
                calorie_count += int(line.strip())
            else:
                calories.append(calorie_count)
                calorie_count = 0
        if calorie_count > 0:
            calories.append(calorie_count)
        
        return calories
    
    def solve1(self, calories):
        return max(calories)

    def solve2(self, calories):
        calories.sort(reverse=True)
        return sum(calories[:3])