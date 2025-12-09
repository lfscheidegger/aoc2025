from typing import List, Tuple, Union
import sys


def transpose_strings(input_chunk: Union[List[str], Tuple[str]]) -> Union[List[str], Tuple[str]]:
    result = []
    for c in range(len(input_chunk[0])):
        line = []
        for r in range(len(input_chunk)):
            line.append(input_chunk[r][c])
        result.append(''.join(line))

    if isinstance(input_chunk, tuple):
        return tuple(result)
    else:
        return result


def part1():
    lines = []
    for line in sys.stdin:
        lines.append([x.strip() for x in line.split()])

    height = len(lines)
    width = len(lines[0])

    total = 0
    for x in range(width):
        numbers = []
        for y in range(height):
            if y == height - 1:
                op = lines[y][x]
                if op == '*':
                    problem = 1
                    for number in numbers:
                        problem *= number
                    total += problem
                else:
                    total += sum(numbers)
            else:
                numbers.append(int(lines[y][x]))

    return total


def part2():
    lines = [line for line in sys.stdin]
    max_length = max(map(lambda l: len(l), lines))
    lines = [line if len(line) == max_length else line + ' '*(max_length-len(line)) for line in lines]

    lines = transpose_strings(lines)
    latest_chunk = []
    chunks = [latest_chunk]

    for l in lines:
        if l.strip() == '':
            latest_chunk = []
            chunks.append(latest_chunk)
        else:
            latest_chunk.append(l.strip())

    final_result = 0
    for c in chunks[:-1]:
        operation = c[0][-1]
        c[0] = c[0][:-1]

        if operation == '+':
            result = 0
        else:
            result = 1

        for entry in c:
            if operation == '+':
                result += int(entry)
            else:
                result *= int(entry)
        final_result += result

    return final_result


print(part2())
