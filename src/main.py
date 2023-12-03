import importlib
import os
import argparse
import datetime
import requests

from termcolor import colored
from os import path
from dotenv import load_dotenv

INIT_CONTENT = 'from .main import *\n'
EG_CONTENT = ''
MAIN_CONTENT = '''import re\n
from ....challenge_runner import ChallengeBase\n
class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, (None, None))
    
    def parse_input(self, lines):
        return lines

    def solve1(self, input):
        return None

    def solve2(self, input):
        return None
'''

INPUT_URL_FMT = 'https://adventofcode.com/{year}/day/{day}/input'
LEVEL_URL_FMT = 'https://adventofcode.com/{year}/day/{day}'
SUBMIT_URL_FMT = 'https://adventofcode.com/{year}/day/{day}/answer'

available_years = list(sorted(os.listdir(path.join(path.dirname(__file__), 'challenges'))))

parser = argparse.ArgumentParser(description='Runs Advent of Code solutions', add_help=True)

subparsers = parser.add_subparsers()

run_parser = subparsers.add_parser('run')
run_parser.add_argument('-s', '--session', help="Advent of code session cookie", nargs='?', default=None)
run_parser.add_argument('-st', '--skip-test', help="Skips the tests", action='store_true')
run_parser.add_argument('-sr', '--skip-run', help="Skips the run of the actual input", action='store_true')
run_parser.add_argument('-ss', '--skip-submit', help="Skips the question if the result should be submitted", action='store_true')
run_parser.add_argument('-ta', '--test-all', help="Runs all tests for all challenges", action='store_true')
run_parser.add_argument('-y', '--year', help="Set the year", type=str, default=str(datetime.date.today().year), choices=available_years)
run_parser.add_argument('days', nargs='*', default=[str(datetime.date.today().day)], help="Days that should be executed, default is current day")

create_parser = subparsers.add_parser('create')
create_parser.add_argument('-s', '--session', help="Advent of code session cookie", nargs='?', default=None)
create_parser.add_argument('day', nargs='?', default=str(datetime.date.today().day), help="Day")
create_parser.add_argument('year', nargs='?', default=str(datetime.date.today().year), help="Year")

def main():
    args = parser.parse_args()

    args.func(args)
    

def execute_run(args):
    if args.test_all:
        test_all(args.year)
    else:
        session = args.session
        if not session and 'AOC_SESSION' in os.environ:
            session = os.environ['AOC_SESSION']
        run(args.year, args.days, not args.skip_test, not args.skip_run, not args.skip_submit, session)

def execute_create(args):
    new_dir = path.join(path.dirname(__file__), 'challenges', args.year, f'day{args.day}')
    if path.isdir(new_dir):
        print(f'== {args.year}/day{args.day} {colored("already exists", "red")} ==')
    else:
        print(f'== Creating {args.year}/day{args.day} ==')
        
        session = args.session
        if not session and 'AOC_SESSION' in os.environ:
            session = os.environ['AOC_SESSION']

        os.makedirs(new_dir, exist_ok=True)
        print(f'{colored("created", "green")} Directory for {args.year}/day{args.day}')

        def write_to_file(name, content):
            with open(path.join(new_dir, name), 'w') as fp:
                fp.write(content)
        
        write_to_file('__init__.py', INIT_CONTENT)
        write_to_file('input.eg', EG_CONTENT)
        write_to_file('main.py', MAIN_CONTENT)
        print(f'{colored("created", "green")} Created __init__.py, input.eg, main.py')

        if session:
            try:
                input_content = requests.get(INPUT_URL_FMT.format(year=args.year, day=args.day), cookies={'session': session}, headers={'User-Agent': 'github.com/alex-zach/advent_of_code by alexander.zach1 (at) gmail.com'}).text
                write_to_file('input.txt', input_content)
                print(f'{colored("Fetched and created", "green")} Created input.txt')
            except:
                session = None
        if not session:
            write_to_file('input.txt', '')
            print(f'{colored("Could not fetch input", "yellow")}, {colored("created", "green")} empty input.txt')

run_parser.set_defaults(func=execute_run)
create_parser.set_defaults(func=execute_create)

def test_all(year):
    available_challenges = list(sorted(os.listdir(path.join(path.dirname(__file__), 'challenges', year))))
    available_challenges.sort(key=lambda x: int(x[3:]))

    print('== Running all Tests ==')

    result_list = []
    for challenge in available_challenges:
        c = importlib.import_module(f'.challenges.{year}.{challenge}', package=__package__).Challenge()
        result_list.append(c.test(prefix = '  '))
    
    flatresults = [r for results in result_list for result in results for r in result ]
    success = len(list(filter(lambda r: r is True, flatresults)))
    failed = len(list(filter(lambda r: r is False, flatresults)))
    skipped = len(list(filter(lambda r: r is None, flatresults)))

    print(f'== {colored("passed", "green")}: {success}, {colored("failed", "red")}: {failed}, {colored("skipped", "yellow")}: {skipped} ==')


def run(year, days, test, run, submit, session):
    for day in days:
        if f'day{day}' not in list(sorted(os.listdir(path.join(path.dirname(__file__), 'challenges', year)))):
            print(f'== {colored(f"Day{day} not available", "yellow")} ==')
        else:
            print(f'== {colored(f"Running Day{day}", "green")} ==')

            result_list = []

            c = importlib.import_module(f'.challenges.{year}.day{day}', package=__package__).Challenge()

            if test:
                result_list.append(c.test(prefix = '  '))
            if run:
                result = c.run(prefix = '  ')
                if submit:
                    if not session:
                        print(f'  {colored("Skipping", "yellow")} submit since no session is provided')
                    else:
                        inp = input('  Submit [1|2|b(oth)|n(o)]: ').lower()
                        submit_lvls = []
                        if inp == '1' or inp in ['b', 'both']:
                            submit_lvls.append(1)
                        if inp == '2' or inp in ['b', 'both']:
                            submit_lvls.append(2)
                        for lvl in submit_lvls:
                            print(f'    Submitting Level {lvl} ... ', end='')

                            submit_response = requests.post(
                                SUBMIT_URL_FMT.format(year=year, day=day),
                                cookies={'session': session},
                                headers={
                                    'User-Agent': 'github.com/alex-zach/advent_of_code by alexander.zach1 (at) gmail.com',
                                    'Referer': LEVEL_URL_FMT.format(year=year, day=day),
                                    'Content-Type': 'application/x-www-form-urlencoded'
                                },
                                data={
                                    'level': lvl,
                                    'answer': result[lvl-1].result
                                }
                            )

                            if submit_response.ok:
                                if "That's not the right answer." in submit_response.text:
                                    print(f'{colored("incorrect solution", "yellow")}.')
                                elif "You gave an answer too recently" in submit_response.text:
                                    print(f'{colored("gave an answer to recently", "yellow")}.')
                                else:
                                    print(f'{colored("done", "green")}.')
                            else:
                                print(f'{colored("failed", "red")}.')

            if test:
                flatresults = [r for results in result_list for result in results for r in result ]
                success = len(list(filter(lambda r: r is True, flatresults)))
                failed = len(list(filter(lambda r: r is False, flatresults)))
                skipped = len(list(filter(lambda r: r is None, flatresults)))
                print(f'== {colored("passed", "green")}: {success}, {colored("failed", "red")}: {failed}, {colored("skipped", "yellow")}: {skipped} ==')
            print()

if __name__ == '__main__':
    load_dotenv()
    main()