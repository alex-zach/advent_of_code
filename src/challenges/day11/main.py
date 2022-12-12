from functools import reduce
from operator import add, mul
import re

from ...challenge_runner import ChallengeBase


class Monkey:
    def __init__(self, id, starting_items, operation, divisible, throw_true, throw_false):
        self.id = id
        self.starting_items = starting_items
        self.operation = operation
        self.divisible = divisible
        self.throw_true = throw_true
        self.throw_false = throw_false
        self.items = [i for i in starting_items]
        self.item_cnt = 0

    def __str__(self):
        return f'Monkey {self.id}: {", ".join([str(s) for s in self.items])}'

    def has_item(self):
        return len(self.items) > 0

    def _pop(self):
        self.item_cnt += 1
        return self.items.pop(0)

    def _next_worry_level(self, div):
        return self.operation(self._pop()) // div

    def next_throw_to(self, div=3):
        worry_level = self._next_worry_level(div)
        return worry_level, self.throw_true if worry_level % self.divisible == 0 else self.throw_false


class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('10605', '2713310158'))

    def parse_input(self, lines):
        p = re.compile(r'Monkey (\d+):\s+Starting items: ([\d, ]+)\s+Operation: new = ([(old)\d]+) ([*+]) ([(old)\d]+)\s+Test: divisible by (\d+)\s+If true: throw to monkey (\d+)\s+If false: throw to monkey (\d+)')

        content = "".join(lines)
        m = p.match(content)

        monkeys = []

        while m:
            op = add if '+' in m.group(4) else mul
            def operation(old, op=op, m=m):
                arg1 = old if m.group(3) == 'old' else int(m.group(3))
                arg2 = old if m.group(5) == 'old' else int(m.group(5))
                return op(arg1, arg2)

            monkeys.append(Monkey(
                int(m.group(1)),
                [int(tok.strip()) for tok in m.group(2).split(',')],
                operation,
                int(m.group(6)),
                int(m.group(7)),
                int(m.group(8))
            ))

            content = content[m.end():].strip()
            m = p.match(content)
            
        return monkeys
            
    def solve1(self, monkeys):
        div = reduce(mul, map(lambda m: m.divisible, monkeys), 1)

        for _ in range(20):
            for monkey in monkeys:
                while monkey.has_item():
                    worry_level, to = monkey.next_throw_to(3)
                    for m2 in monkeys:
                        if m2.id == to:
                            m2.items.append(worry_level % div)
                            break
        
        itemcnts = [monkey.item_cnt for monkey in monkeys]
        itemcnts.sort(reverse=True)
        
        return itemcnts[0] * itemcnts[1]
    
    def solve2(self, monkeys):
        div = reduce(mul, map(lambda m: m.divisible, monkeys), 1)

        for i in range(10000):
            for monkey in monkeys:
                while monkey.has_item():
                    worry_level, to = monkey.next_throw_to(1)
                    for m2 in monkeys:
                        if m2.id == to:
                            m2.items.append(worry_level % div)
                            break
        
        itemcnts = [monkey.item_cnt for monkey in monkeys]
        itemcnts.sort(reverse=True)
        
        return itemcnts[0] * itemcnts[1]