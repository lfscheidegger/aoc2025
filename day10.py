from dataclasses import dataclass
from functools import cache
from itertools import combinations
from typing import Dict, Set, Tuple, List

import sys


@dataclass(frozen=True)
class Edge:
    next_node_id: str
    cost: int


Graph = Dict[str, Set[Edge]]


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
    BIG_NUMBER = 2**64 - 1
    
    @dataclass(frozen=True)
    class ButtonPattern:
        pattern: Tuple[int]
        button_cost: int

        @staticmethod
        def from_input_line(line: str) -> Tuple['ButtonPattern']:
            state_token = tuple(int(x) for x in line.split()[-1][1:-1].split(','))
            button_tokens = line.split()[1:-1]
            button_tokens = list(map(lambda bt: tuple(int(x) for x in bt[1:-1].split(',')), button_tokens))

            result = []
            for combination_size in range(len(button_tokens) + 1):
                for button_combination in combinations(button_tokens, combination_size):
                    pattern = [0] * len(state_token)
                    for button in button_combination:
                        for circuit in button:
                            pattern[circuit] += 1

                    result.append(ButtonPattern(pattern=pattern, button_cost=len(button_combination)))

            return tuple(result)

    def all_zero(state: Tuple[int]) -> bool:
        return all(map(lambda value: value == 0, state))

    def all_even(state: Tuple[int]) -> bool:
        return all(map(lambda value: value % 2 == 0, state))

    def valid_state(state: Tuple[int]) -> bool:
        return all(map(lambda value: value >= 0, state))

    def get_initial_state(line: str) -> Tuple[int]:
        return tuple(int(x) for x in line.split()[-1][1:-1].split(','))

    def get_halved_state(state: Tuple[int]) -> Tuple[int]:
        assert all_even(state)
        return tuple(x // 2 for x in state)
    
    def get_next_state(state: Tuple[int], pattern: ButtonPattern) -> Tuple[int]:
        return tuple([state[idx] - pattern.pattern[idx] for idx in range(len(state))])

    #@cache    
    def solve_single(state: Tuple[int], patterns: Tuple[ButtonPattern], depth: int = 0, so_far: int = 0) -> int:
        # print(f'{4 * depth * ' '}{state} ({so_far})')
        if not valid_state(state):
            return BIG_NUMBER
        
        if all_zero(state):
            return 0

        result = BIG_NUMBER
        for pattern in patterns:
            next_state = get_next_state(state, pattern)
            if not all_even(next_state):
                continue

            if not valid_state(next_state):
                continue

            next_state = get_halved_state(next_state)
            # print(f'{4 * depth * ' '}ns -> {next_state}')
            result = min(result, pattern.button_cost + 2 * solve_single(next_state, patterns, depth + 1, so_far + pattern.button_cost))

        return result

    def solve_line(line: str) -> int:
        patterns = ButtonPattern.from_input_line(line)
        state = get_initial_state(line)

        return solve_single(state, patterns)

    result = 0
    for idx, line in enumerate(sys.stdin):
        for_line = solve_line(line)
        print(idx, for_line)
        result += for_line

    print()
    return result


print(part2())
