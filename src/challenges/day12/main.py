from platform import node
import re

from ...challenge_runner import ChallengeBase


class Graph:
    class Node:
        def __init__(self, name, successors=None):
            self.name = name
            if successors == None:
                self.successors = []
            else:
                self.successors = successors

        def add_successor(self, succ, dist=1):
            self.successors.append((succ, dist))

        def __str__(self) -> str:
            return f'node{self.name}'

    def __init__(self, nodes=None):
        if nodes == None:
            self.nodes = {}
        else:
            self.nodes = nodes

    def add_node(self, node):
        self.nodes[node.name] = node


def a_star(graph, start_name, end_name, h):
    start = graph.nodes[start_name]
    end = graph.nodes[end_name]

    open_set = set([start])
    closed_set = set([])

    gs = {}
    gs[start_name] = 0

    hs = {}
    for _, node in graph.nodes.items():
        hs[node.name] = h(node, end)

    prev = {}
    prev[start.name] = None

    while len(open_set) > 0:
        nextnode = None

        # Node with minimal f
        for node in open_set:
            if nextnode == None or gs[node.name] + hs[node.name] < gs[nextnode.name] + hs[nextnode.name]:
                nextnode = node
    
        if nextnode.name == end_name:
            path = [nextnode]
            while prev[path[-1].name] is not None:
                path.append(prev[path[-1].name])
            
            path.reverse()

            return path

        for neighbor, weight in nextnode.successors:
            if neighbor not in open_set and neighbor not in closed_set:
                open_set.add(neighbor)
                prev[neighbor.name] = nextnode
                gs[neighbor.name] = gs[nextnode.name] + weight
            
            elif gs[neighbor.name] > gs[nextnode.name] + weight:
                prev[neighbor.name] = nextnode
                gs[neighbor.name] = gs[nextnode.name] + weight

                if neighbor in closed_set:
                    closed_set.remove(neighbor)
                    open_set.add(neighbor)

        open_set.remove(nextnode)
        closed_set.add(nextnode)

    return None


def heur(start, end):
    p = re.compile(f'\((\d+), (\d+)\)')
    startm = p.match(start.name)
    endm = p.match(end.name)

    return abs(int(startm.group(1)) - int(endm.group(2))) + abs(int(startm.group(2)) - int(endm.group(2)))


class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('31', '29'))

    def parse_input(self, lines):
        start = (0,0)
        end = (0,0)

        grid = []

        for i, line in enumerate(lines):
            gridline = []
            for j, c in enumerate(line.strip()):
                if c == "S":
                    gridline.append(0)
                    start = (i,j)
                elif c == "E":
                    gridline.append(ord('z') - ord('a'))
                    end = (i,j)
                else:
                    gridline.append(ord(c) - ord('a'))
            
            if len(gridline) > 0:
                grid.append(gridline)

        return grid, start, end
            
    def solve1(self, input):
        grid, start, end = input
        dirs = ((0,1),(1,0),(0,-1),(-1,0))

        nodes = {}

        for i, line in enumerate(grid):
            for j, _ in enumerate(line):
                name = str((i,j))
                nodes[name] = Graph.Node(name)
        
        for i, line in enumerate(grid):
            for j, cell in enumerate(line):
                for dirlr, dirud in dirs:
                    if i + dirlr < len(grid) and j + dirud < len(grid[i + dirlr]) \
                        and i + dirlr >= 0 and j + dirud >= 0 \
                        and grid[i + dirlr][j + dirud] - cell <= 1:
                        
                        nodes[str((i,j))].add_successor(nodes[str((i + dirlr, j + dirud))])

        graph = Graph(nodes)

        path = a_star(graph, str(start), str(end), heur)

        return len(path) - 1
    
    def solve2(self, input):
        grid, _, end = input
        dirs = ((0,1),(1,0),(0,-1),(-1,0))
        starts = []

        nodes = {}

        for i, line in enumerate(grid):
            for j, cell in enumerate(line):
                name = str((i,j))
                nodes[name] = Graph.Node(name)
                if cell == 0:
                    starts.append(str((i,j)))
        
        for i, line in enumerate(grid):
            for j, cell in enumerate(line):
                for dirlr, dirud in dirs:
                    if i + dirlr < len(grid) and j + dirud < len(grid[i + dirlr]) \
                        and i + dirlr >= 0 and j + dirud >= 0 \
                        and grid[i + dirlr][j + dirud] - cell <= 1:
                        
                        nodes[str((i,j))].add_successor(nodes[str((i + dirlr, j + dirud))])

        graph = Graph(nodes)

        paths = []
        while len(starts) > 0:
            start = starts.pop(0)
            path = a_star(graph, str(start), str(end), heur)

            if path:
                maxi = 0
                for i, p in enumerate(path):
                    if p in starts:
                        starts.remove(p)
                        maxi = i
                paths.append(path[maxi:])

        return min([len(path) for path in paths]) - 1
        

