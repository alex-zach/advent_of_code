import re

from math import inf
from itertools import product
from ....challenge_runner import ChallengeBase

def dijkstra(valves, start):
    open_set = set(valves.keys())

    dist = {}
    for v in valves: dist[v] = inf
    dist[start] = 0

    prev = {}
    prev[start] = None

    while len(open_set) > 0:
        node = None

        for n in open_set:
            if node is None or dist[n] < dist[node]:
                node = n
        
        for neighbor in valves[node][1]:
            if neighbor in open_set:
                new_dist = dist[node] + 1
                if new_dist < dist[neighbor]:
                    dist[neighbor] = new_dist
                    prev[neighbor] = node

        open_set.remove(node)

    return dist, prev


class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('1651', None))
    
    def parse_input(self, lines):
        p = re.compile(r'Valve (\w+) has flow rate=(\d+); tunnels? leads? to valves? ([\w,\s]+)')
        valves = {}
        for line in lines:
            m = p.match(line)
            if m:
                valves[m.group(1).strip()] = (int(m.group(2)), list(map(lambda s: s.strip(), m.group(3).split(','))))
        
        return valves

    def solve1(self, valves):
        minutes = 30

        working_valves = [v for v in valves if valves[v][0] > 0] + ['AA']
        clean_valves = {}

        for v in working_valves:
            dists,_ = dijkstra(valves, v)
            clean_valves[v] = (valves[v][0], {})
            for n in working_valves:
                if n == v: continue
                clean_valves[v][1][n] = dists[n]

        def recursion(remaining_minutes, current_valve, open_valves, total_flow):
            fpm = sum([clean_valves[v][0] for v in open_valves])

            if remaining_minutes == 0:
                return 0

            max_flow = total_flow + remaining_minutes * fpm

            if len(open_valves) + 1 < len(working_valves):
                for next_valve in clean_valves[current_valve][1]:
                    if next_valve in open_valves: 
                        continue

                    open_duration = clean_valves[current_valve][1][next_valve]+1
                    if open_duration > remaining_minutes:
                        continue

                    f = recursion(remaining_minutes-open_duration, next_valve, [next_valve, *open_valves], total_flow + open_duration * fpm)

                    if f > max_flow:
                        max_flow = f

            return max_flow

        res = recursion(minutes, 'AA', [], 0)
        return res

    def solve2(self, valves):
        minutes = 26

        working_valves = [v for v in valves if valves[v][0] > 0] + ['AA']
        clean_valves = {}

        for v in working_valves:
            dists,_ = dijkstra(valves, v)
            clean_valves[v] = (valves[v][0], {})
            for n in working_valves:
                if n == v: continue
                clean_valves[v][1][n] = dists[n]

        def recursion(remaining_minutes, current_valve1, current_valve2, open_valves, total_flow):
            fpm = sum([clean_valves[v][0] for v in open_valves])

            if remaining_minutes == 0:
                return 0

            max_flow = total_flow + remaining_minutes * fpm

            if len(open_valves) + 1 < len(working_valves):
                

            return max_flow

        res = recursion(minutes, 'AA', [], 0)
        return res
