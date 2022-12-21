from copy import deepcopy
from math import ceil
from operator import add, sub, mul, truediv as div
import re

from ....challenge_runner import ChallengeBase

class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('152', '301'))
    
    def parse_input(self, lines):
        p = re.compile(r'(\w{4}): (((\w{4}) ([+-/*]) (\w{4}))|(\d+))')

        monkeys = {}
        operations = {'+': add, '-': sub, '*': mul, '/': div}

        for line in lines:
            m = p.match(line)
            if m:
                if m.group(3):
                    monkeys[m.group(1)] = (m.group(4), operations[m.group(5)], m.group(6))
                elif m.group(7):
                    monkeys[m.group(1)] = int(m.group(7))

        return monkeys

    def solve1(self, monkeys):

        def calculate(monkey, monkeys):
            item = monkeys[monkey]
            if type(item) is not tuple:
                return item
            m1, op, m2 = item
            res = op(calculate(m1, monkeys), calculate(m2, monkeys))
            monkeys[monkey] = res
            return res

        return int(calculate('root', monkeys))

    def solve2(self, monkeys):
        def calculate(monkey, monkeys):
            item = monkeys[monkey]
            if type(item) is not tuple:
                return item
            m1, op, m2 = item
            c1 = calculate(m1, monkeys)
            c2 = calculate(m2, monkeys)
            
            if type(c1) in [int, float] and type(c2) in [int, float] and op is not str:
                res = op(c1, c2)
            else:
                res = [c1, op, c2]
            
            monkeys[monkey] = res
            return res

        monkeys['humn'] = 'humn'
        monkeys['root'] = (monkeys['root'][0], '==', monkeys['root'][2])

        tree = calculate('root', monkeys)
        tree[1] = sub
        print(tree)

        def f(humn):
            def rec(tree, humn):
                if tree[0] == 'humn':
                    tree[0] = humn
                if tree[2] == 'humn':
                    tree[2] = humn
                
                if type(tree[0]) not in [int, float]:
                    tree[0] = rec(tree[0], humn)         
                if type(tree[2]) not in [int, float]:
                    tree[2] = rec(tree[2], humn)
                return tree[1](tree[0], tree[2])
            return rec(deepcopy(tree), humn)

        def secant_method(f, x0, x1, iterations):
            for i in range(iterations):
                x2 = x1 - f(x1) * (x1 - x0) / float(f(x1) - f(x0))
                x0, x1 = x1, x2
                if (x0 - x1) == 0:
                    return x2
            return x2
        
        return int(secant_method(f, 0, 1E10, 1000))
                    
        # Doesn't work - dont know why:
        # tree = calculate('root', monkeys)
        # calc_side, res_side = 2, 0
        # if str(tree).index('humn') < str(tree).index('=='):
        #     calc_side, res_side = 0, 2
    
        # inverse_op = {add: sub, sub: add, mul: div, div: mul}

        # while type(tree[calc_side]) is not str:
        #     nr_side, rest = (0, 2) if type(tree[calc_side][0]) in [int, float] else (2, 0)
        #     tree[res_side] = ceil(inverse_op[tree[calc_side][1]](tree[res_side], tree[calc_side][nr_side]))
        #     tree[calc_side] = tree[calc_side][rest]

        # return int(tree[res_side])