from itertools import permutations
from math import ceil, floor

with open("input18.txt") as f:
    lines = [eval(line.rstrip()) for line in f]


class Node:

    def __init__(self, left=None, right=None, value=None):
        self.left = left
        self.right = right
        self.value = value

    def __str__(self):
        if self.value is not None:
            return str(self.value)
        else:
            return f"[{self.left}, {self.right}]"

    @staticmethod
    def of(elem):
        if isinstance(elem, list):
            return Node(left=Node.of(elem[0]), right=Node.of(elem[1]))
        else:
            return Node(value=elem)


class Exploder:

    def reset(self):
        self.prev_node = None
        self.to_add = None
        self.done = False

    def explode(self, node, level=0):
        if self.done:
            next_node = node
        elif node.value is None:
            next_node = self.explode_pair(node, level)
        else:
            next_node = self.explode_leaf(node)
        return next_node

    def explode_pair(self, node, level):
        if level == 4 and self.to_add is None:
            self.to_add = node.right.value
            if self.prev_node:
                self.prev_node.value += node.left.value
            next_node = Node(value=0)
        else:
            left = self.explode(node.left, level + 1)
            if self.done:
                next_node = Node(left=left, right=node.right)
            else:
                right = self.explode(node.right, level + 1)
                next_node = Node(left=left, right=right)
        return next_node

    def explode_leaf(self, node):
        if self.to_add is not None:
            node.value += self.to_add
            self.done = True
        else:
            self.prev_node = node
        return node


def split_node(node):
    split = False
    if node.value is not None:
        if node.value >= 10:
            next_node = Node(
                left=Node(value=floor(node.value / 2)),
                right=Node(value=ceil(node.value / 2))
            )
            split = True
        else:
            next_node = node
    else:
        left, split = split_node(node.left)
        if split:
            next_node = Node(left=left, right=node.right)
        else:
            right, split = split_node(node.right)
            next_node = Node(left=left, right=right)
    return next_node, split


def redux(node):
    exploder = Exploder()
    while True:
        exploder.reset()
        node = exploder.explode(node)
        if exploder.done or exploder.to_add is not None:
            continue
        node, changed = split_node(node)
        if not changed:
            break
    return node


def magnitude(node):
    if node.value is not None:
        return node.value
    return 3 * magnitude(node.left) + 2 * magnitude(node.right)


root = Node.of(lines[0])
for line in lines[1:]:
    root = redux(Node(left=root, right=Node.of(line)))
print(magnitude(root))
print(max(
    magnitude(redux(Node(left=Node.of(a), right=Node.of(b))))
    for a, b in permutations(lines, 2)
))
