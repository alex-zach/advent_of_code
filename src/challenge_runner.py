from __future__ import annotations
from copy import deepcopy
from functools import wraps
from os import path
from time import time
from termcolor import colored


class Res:
    def __init__(self, dur, res):
        self.duration = dur
        self.result = res

    def format_duration(self):
        if self.duration < 0.5:
            return colored(f'{round(self.duration * 1000, 2)} ms', 'green')
        if self.duration < 1:
            return colored(f'{round(self.duration * 1000, 2)} ms', 'yellow')
        return colored(f'{round(self.duration, 2)} s', 'red')


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        res = func(*args, **kwargs)
        duration = time() - start
        return Res(duration, res)

    return wrapper


def is_eg_param(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    wrapper.eg_param = True
    return wrapper


class ChallengeBase:
    def __init__(self, file, expected_eg_outputs, eg_input_filenames=None) -> None:
        self._dirname = path.dirname(file)
        self._challenge_name = f'{path.basename(path.dirname(self._dirname))}-{path.basename(self._dirname)}'
        self._eg_input_filenames = eg_input_filenames \
                                        if eg_input_filenames is not None \
                                        else ['input.eg']
        self._expected_eg_outputs = expected_eg_outputs \
                                        if hasattr(expected_eg_outputs, '__iter__') and hasattr(expected_eg_outputs, '__len__') and type(expected_eg_outputs[0]) in [list, tuple] \
                                        else [expected_eg_outputs]

        if (len(self._expected_eg_outputs) != len(self._eg_input_filenames)):
            raise Exception('invalid eg params')

    def parse_input(self, lines):
        return None

    def solve1(self, parsed_input):
        return None

    def solve2(self, parsed_input):
        return None

    def _get_input(self, input_name):
        with open(path.join(self._dirname, input_name), 'r') as f:
            lines = f.readlines()
            return self.parse_input(lines)

    def _solve(self, input_name, eg, skip1=False, skip2=False):
        inp = self._get_input(input_name)
        inp2 = deepcopy(inp)

        if hasattr(self.solve1, 'eg_param') and self.solve1.eg_param:
            inp = (inp, eg)
        else:
            inp = (inp,)
        
        if hasattr(self.solve2, 'eg_param') and self.solve2.eg_param:
            inp2 = (inp2, eg)
        else:
            inp2 = (inp2,)

        return timed(self.solve1)(*inp) if not skip1 else Res(0,None), timed(self.solve2)(*inp2) if not skip2 else Res(0,None)

    def test(self, prefix="", output=True):
        solutions = []
        results = []

        for i, file in enumerate(self._eg_input_filenames):
            solutions.append(self._solve(file, True, self._expected_eg_outputs[i][0] is None, self._expected_eg_outputs[i][1] is None))
            results.append([None, None])

        if output:
            print(f'{prefix}{self._challenge_name} [test]')

        for lvl in range(2):
            if output:
                print(f'{prefix}│')

            if all([solution[lvl].result is None for solution in solutions]):
                if output:
                    print(f'{prefix}├── {lvl+1} {colored("skipped", "yellow")}')
            else:
                for case in range(len(solutions)):
                    if solutions[case][lvl].result is None:
                        if output and self._expected_eg_outputs[case][lvl] is not None: 
                            print(f'{prefix}├── {lvl+1}{f"[Case {case+1}]" if len(solutions) > 1 else ""} {colored("skipped", "yellow")}')
                        if self._expected_eg_outputs[case][lvl] is None:
                            results[case][lvl] = -1
                    elif str(solutions[case][lvl].result) == str(self._expected_eg_outputs[case][lvl]):
                        if output:
                            print(f'{prefix}├── {lvl+1}{f"[Case {case+1}]" if len(solutions) > 1 else ""} {colored("passed", "green")} ({solutions[case][lvl].format_duration()})')
                        results[case][lvl] = True
                    else:
                        if output:
                            print(f'{prefix}├─┬ {lvl+1}{f"[Case {case+1}]" if len(solutions) > 1 else ""} {colored("failed", "red")} ({solutions[case][lvl].format_duration()})')
                            print(f'{prefix}│ ├─ expected "{colored(self._expected_eg_outputs[case][lvl], "green")}"')
                            print(f'{prefix}│ ├─ got      "{colored(solutions[case][lvl].result, "red")}"')
                        results[case][lvl] = False

        if output:
            print()
        
        return results

    def run(self, prefix="", output=True):
        solution = self._solve('input.txt', False)

        if output:
            print(f'{prefix}{self._challenge_name} [run]')

            for lvl in range(2):
                print(f'{prefix}│')

                if solution[lvl] is None: 
                    print(f'{prefix}├── {lvl+1} {colored("skipped", "yellow")}')
                else:
                    print(f'{prefix}├── {lvl+1} {colored(solution[lvl].result, "blue")} ({solution[lvl].format_duration()})')
            
            print()

        return solution
