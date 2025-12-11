from dataclasses import dataclass
from typing import Dict, Set, Tuple, List
import heapq


@dataclass(frozen=True)
class Edge:
    next_node_id: str
    cost: int


Graph = Dict[str, Set[Edge]]


def dijkstra(starting_point: str, graph: Graph) -> Dict[str, Tuple[int, List[str]]]:
    result = {}

    heap = [(0, starting_point, [])]
    while len(heap) != 0:
        best_cost, node, path = heapq.heappop(heap)

        if node in result:
            # already processed
            continue

        result[node] = (best_cost, path)

        for neighbor in graph.get(node, set()):
            next_node = neighbor.next_node_id
            next_cost = best_cost + neighbor.cost
            heapq.heappush(heap, (next_cost, next_node, path + [next_node]))

    return result


import sys


def edge_str_to_number(edge_str: str) -> int:
    result = 0
    for idx in edge_str[1:-1].split(","):
        result += 2 ** int(idx)

    return result


def state_str_to_number(state_str: str) -> int:
    result = 0
    for idx, token in enumerate(state_str[1:-1]):
        if token == '#':
            result += 2 ** idx

    return result


def part1():
    def solve_line(line: str) -> int:
            tokens = line.split()[:-1]
            goal_state = tokens[0]

            goal_state = state_str_to_number(goal_state)

            edges = [edge_str_to_number(edge_str) for edge_str in tokens[1:]]

            queue = [(0, 0)]
            found = set()
            while True:
                assert len(queue) > 0
                state, count = queue[0]        
                queue = queue[1:]

                if state in found:
                    continue

                for edge in edges:
                    next_state = state ^ edge
                    if next_state == goal_state:
                        return count + 1

                    queue.append((next_state, count + 1))

                found.add(state)
    result = 0

    for idx, line in enumerate(sys.stdin):
        for_line = solve_line(line)
        result += for_line

    return result


def part2():
    def get_next_state(state, edge):
        return tuple([state[idx] + 1 if idx in edge else state[idx] for idx in range(len(state))])
    
    def solve_line(line: str) -> int:
        tokens = line.split()[1:]
        goal_state = tuple(int(x) for x in tokens[-1][1:-1].split(','))

        edges = list(map(lambda t: set(int(x) for x in t[1:-1].split(',')), tokens[:-1]))

        initial_state = tuple([0] * len(goal_state))

        queue = [(initial_state, 0)]
        found = set()

        while True:
            assert len(queue) > 0
            state, count = queue[0]        
            queue = queue[1:]

            if state in found:
                continue

            found.add(state)
            if any(map(lambda idx: goal_state[idx] < state[idx], range(len(state)))):                
                continue

            for edge in edges:
                next_state = get_next_state(state, edge)
                if next_state == goal_state:
                    return count + 1

                queue.append((next_state, count + 1))

    result = 0

    for idx, line in enumerate(sys.stdin):
        print(idx)
        for_line = solve_line(line)
        print(for_line)
        result += for_line

    print()
    return result

print(part2())
