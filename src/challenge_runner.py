from copy import deepcopy
from os import path
from termcolor import colored


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

    def _solve(self, input_name):
        inp = self._get_input(input_name)
        inp2 = deepcopy(inp)

        return self.solve1(inp), self.solve2(inp2)

    def test(self, prefix="", output=True):
        solutions = []
        results = []

        for file in self._eg_input_filenames:
            solutions.append(self._solve(file))
            results.append([None, None])

        if output:
            print(f'{prefix}{self._challenge_name} [test]')


        for lvl in range(2):
            if output:
                print(f'{prefix}│')

            if all([solution[lvl] is None for solution in solutions]):
                print(f'{prefix}├── {lvl+1} {colored("skipped", "yellow")}')
            else:
                for case in range(len(solutions)):
                    if solutions[case][lvl] is None and output: 
                        print(f'{prefix}├── {lvl+1}{f"[Case {case+1}]" if len(solutions) > 1 else ""} {colored("skipped", "yellow")}')
                    elif str(solutions[case][lvl]) == str(self._expected_eg_outputs[case][lvl]) and output:
                        print(f'{prefix}├── {lvl+1}{f"[Case {case+1}]" if len(solutions) > 1 else ""} {colored("passed", "green")}')
                        results[case][lvl] = True
                    else:
                        if output:
                            print(f'{prefix}├─┬ {lvl+1}{f"[Case {case+1}]" if len(solutions) > 1 else ""} {colored("failed", "red")}')
                            print(f'{prefix}│ ├─ expected "{colored(self._expected_eg_outputs[case][lvl], "green")}"')
                            print(f'{prefix}│ ├─ got      "{colored(solutions[case][lvl], "red")}"')
                        results[case][lvl] = False

        if output:
            print()
        
        return results

    def run(self, prefix="", output=True):
        solution = self._solve('input.txt')

        if output:
            print(f'{prefix}{self._challenge_name} [run]')

        for lvl in range(2):
            if output:
                print(f'{prefix}│')

            if solution[lvl] is None: 
                print(f'{prefix}├── {lvl+1} {colored("skipped", "yellow")}')
            else:
                print(f'{prefix}├── {lvl+1} {colored(solution[lvl], "blue")}')
        
        if output:
            print()

        return solution
