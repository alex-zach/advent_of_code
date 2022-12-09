from operator import contains
import re

from ...challenge_runner import ChallengeBase


class Node:
    def __init__(self, name, node_type, size=0, children=None, parent=None):
        self.name = name
        self.node_type = node_type
        self.size = size
        self.children = children
        self.parent = parent

    def is_file(self):
        return self.node_type == 'file'

    def is_dir(self):
        return self.node_type =='dir'

    def add_child(self, node):
        if type(self.children) == list:
            self.children.append(node)
        else:
            raise Exception()

    def get_child(self, name, node_type = None):
        if type(self.children) == list:
            for c in self.children:
                if c.name == name and (node_type is None or c.node_type == node_type):
                    return c
            return None
        else:
            raise Exception()

    def __str__(self):
        if self.is_dir():
            return f'dir {self.name} {str(list(map(lambda e: str(e), self.children)))}'
        elif self.is_file():
            return f'file {self.name}'

    def print_tree(self, prefix = ''):
        if self.is_dir():
            print(f'{prefix}- {self.name} (dir)')
            for child in self.children:
                child.print_tree(prefix = prefix + '  ')
        elif self.is_file():
            print(f'{prefix}- {self.name} (file, size={self.size})')

    def total_size(self):
        if self.is_dir():
            return sum(map(lambda c: c.total_size(), self.children))
        if self.is_file():
            return self.size

class File(Node):
    def __init__(self, name, size, parent):
        super().__init__(name, 'file', size, parent=parent)


class Directory(Node):
    def __init__(self, name, children = None, parent = None):
        if children is None:
            children = []
        super().__init__(name, 'dir', children=children, parent=parent)


class Challenge(ChallengeBase):
    def __init__(self):
        super().__init__(__file__, ('95437', '24933642'))

    def parse_input(self, lines):
        cd_p = re.compile(r'\$ cd\s([/\w\d\.]*)')
        ls_p = re.compile(r'\$ ls')
        dir_p = re.compile(r'dir ([/\w\d\.]+)')
        file_p = re.compile(r'(\d+) ([/\w\d\.]+)')

        root = Directory(name=cd_p.match(lines[0]).group(1))
        cur_dir = root

        i = 1
        while i < len(lines):
            line = lines[i]

            cd_m = cd_p.match(line)
            if cd_m:
                target = cd_m.group(1)

                if target.startswith('/'):
                    cur_dir = root
                    parts = list(filter(lambda p: len(p) > 0, target.split('/')))
                    for part in parts:
                        if part == '.':
                            continue
                        elif part == '..':
                            cur_dir = cur_dir.parent if cur_dir.parent else cur_dir
                            continue
                        else:
                            c = cur_dir.get_child(part, 'dir')
                            if c is None:
                                c = Directory(part, parent=cur_dir)
                                cur_dir.add_child(c)
                            cur_dir = c
                elif target == '..':
                    cur_dir = cur_dir.parent if cur_dir.parent else cur_dir
                elif target != '.':
                    c = cur_dir.get_child(target, 'dir')
                    if c is None:
                        c = Directory(target, parent=cur_dir)
                        cur_dir.add_child(c)
                    cur_dir = c

                i += 1
                continue
            
            ls_m = ls_p.match(line)
            if ls_m:
                while i+1 < len(lines) and not lines[i+1].startswith('$'):
                    i += 1
                    dir_m = dir_p.match(lines[i])
                    if dir_m:
                        name = dir_m.group(1)
                        c = cur_dir.get_child(name, 'dir')
                        if c is None:
                            c = Directory(name, parent=cur_dir, children=[])
                            cur_dir.add_child(c)
                        continue

                    file_m = file_p.match(lines[i])
                    if file_m:
                        size, name = file_m.group(1), file_m.group(2)
                        c = cur_dir.get_child(name, 'file')
                        if c is None:
                            c = File(name, int(size), cur_dir)
                            cur_dir.add_child(c)
                i += 1
        return root
            
    def solve1(self, root):
        total = 0
        todo = [root]

        while len(todo) > 0:
            cur = todo.pop()
            todo += list(filter(lambda x: x.is_dir(), cur.children))

            if cur.total_size() < 100000:
                total += cur.total_size()

        return total


    def solve2(self, root):
        min_to_del = root.total_size()
        needed = 30000000 - (70000000 - min_to_del)
        todo = [root]

        while len(todo) > 0:
            cur = todo.pop()
            todo += list(filter(lambda x: x.is_dir(), cur.children))

            if cur.total_size() >= needed:
                min_to_del = min(min_to_del, cur.total_size())

        return min_to_del

