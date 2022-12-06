import importlib
import os
import argparse
import datetime

from termcolor import colored
from os import path


parser = argparse.ArgumentParser(description='Runs Advent of Code solutions', add_help=True)

parser.add_argument('-st', '--skip-test', help="Skips the tests", action='store_true')
parser.add_argument('-sr', '--skip-run', help="Skips the run of the actual input", action='store_true')
parser.add_argument('-ta', '--test-all', help="Runs all tests for all challenges", action='store_true')
parser.add_argument('days', nargs='*', default=[str(datetime.date.today().day)], help="Days that should be executed, default is current day")

if __name__ == '__main__':
    args = parser.parse_args()

    available_challenges = list(sorted(os.listdir(path.join(path.dirname(__file__), 'challenges'))))

    if args.test_all:
        print('== Running all Tests ==')
        result_list = []
        for challenge in available_challenges:
            c = importlib.import_module(f'.challenges.{challenge}', package=__package__).Challenge()
            result_list.append(c.test(prefix = '  '))
        
        flatresults = [r for results in result_list for result in results for r in result ]
        success = len(list(filter(lambda r: r is True, flatresults)))
        failed = len(list(filter(lambda r: r is False, flatresults)))
        skipped = len(list(filter(lambda r: r is None, flatresults)))
        print(f'== {colored("passed", "green")}: {success}, {colored("failed", "red")}: {failed}, {colored("skipped", "yellow")}: {skipped} ==')
    else:
        for day in args.days:
            if f'day{day}' not in available_challenges:
                print(f'== {colored(f"Day{day} not available", "yellow")} ==')
            else:
                print(f'== {colored(f"Running Day{day}", "green")} ==')

                result_list = []

                c = importlib.import_module(f'.challenges.day{day}', package=__package__).Challenge()

                if not args.skip_test:
                    result_list.append(c.test(prefix = '  '))
                if not args.skip_run:
                    c.run(prefix = '  ')

                if not args.skip_test:
                    flatresults = [r for results in result_list for result in results for r in result ]
                    success = len(list(filter(lambda r: r is True, flatresults)))
                    failed = len(list(filter(lambda r: r is False, flatresults)))
                    skipped = len(list(filter(lambda r: r is None, flatresults)))
                    print(f'== {colored("passed", "green")}: {success}, {colored("failed", "red")}: {failed}, {colored("skipped", "yellow")}: {skipped} ==')
                print()
                