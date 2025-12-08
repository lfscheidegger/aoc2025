import sys


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
    lines = [line.strip() for line in sys.stdin]
    max_length = max(map(lambda l: len(l), lines))
    lines = [line if len(line) == max_length else line + ' '*(max_length-len(line)) for line in lines]

    height = len(lines)
    width = max_length

    for x in range(width-1, -1, -1):
        print(x)
    #head = lines[:-1]
    #head.reverse()

    #lines = head + [lines[-1]]

    #lines.reverse()
    #for line in lines:
    #    print(f'[{line}]')
    


print(part2())
