import re

from ...challenge_runner import ChallengeBase


class Instruction:
    def __init__(self, steps):
        self.steps = steps
        self.cnt = 0

    def step(self, registers):
        self.cnt += 1
        if self.cnt == self.steps:
            self.cnt = 0
            return True
        return False


class NoopInstruction(Instruction):
    _pattern = re.compile(r'noop')

    def __init__(self):
        super().__init__(1)

    @classmethod
    def from_string(cls, str):
        if cls._pattern.match(str):
            return NoopInstruction()
        return None

    def __str__(self):
        return 'noop'


class AddXInstruction(Instruction):
    _pattern = re.compile(r'addx (-?\d+)')

    def __init__(self, inc):
        super().__init__(2)
        self.inc = inc

    def step(self, registers):
        if super().step(registers):
            registers['X'] += self.inc
            return True
        return False

    @classmethod
    def from_string(cls, str):
        m = cls._pattern.match(str)
        if m:
            return AddXInstruction(int(m.group(1)))
        return None

    def __str__(self):
        return f'addx {self.inc}'


class Executor:
    def __init__(self, instructions):
        self.instructions = instructions
        self.ip = 0
        self.registers = {'X': 1}
        self.stepcnt = 0
    
    def step(self, n=1):
        while n > 0:
            self.stepcnt += 1
            if self.instructions[self.ip].step(self.registers):
                self.ip += 1
            n -= 1

    def done(self):
        return self.ip >= len(self.instructions)

eg2_output = '\n'+\
    "##..##..##..##..##..##..##..##..##..##..\n" +\
    "###...###...###...###...###...###...###.\n" +\
    "####....####....####....####....####....\n" +\
    "#####.....#####.....#####.....#####.....\n" +\
    "######......######......######......####\n" +\
    "#######.......#######.......#######....."

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('13140', eg2_output))

    def parse_input(self, lines):
        available_instructions = [NoopInstruction, AddXInstruction]
        instructions = []

        for line in lines:
            for ins in available_instructions:
                instance = ins.from_string(line)
                if instance:
                    instructions.append(instance)
                    break

        return instructions
            
    def solve1(self, instructions):
        executor = Executor(instructions)
        total = 0

        executor.step(19)
        for i in range(20, 220, 40):
            total += i * executor.registers['X']
            executor.step(40)
        total += 220 * executor.registers['X']
        
        return total
    
    def solve2(self, instructions):
        executor = Executor(instructions)
        result = ''
        
        cnt = 0
        while not executor.done():
            sprite_start = executor.registers['X'] - 1

            if cnt > 0 and cnt % 40 == 0:
                result += '\n'

            temp = cnt % 40 - sprite_start
            if temp >= 0 and temp <= 2:
                result += '#'
            else:
                result += '.'
                
            cnt += 1
            executor.step()
        
        return '\n' + result
