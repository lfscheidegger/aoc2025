from collections import defaultdict
import sys


def part1():
    coords = [(int(x), int(y)) for x, y in [l.strip().split(",") for l in sys.stdin]]
    distances = []

    for i in range(len(coords)):
        for j in range(1, len(coords)):
            left, right = coords[i], coords[j]

            distances.append(((i, j), abs(1 + coords[i][0] - coords[j][0]) * abs(1 + coords[i][1] - coords[j][1])))

    distances.sort(key = lambda d: -d[1])

    return distances[0][1]


def part2():
    coords = [(int(x), int(y)) for x, y in [l.strip().split(",") for l in sys.stdin]]

    min_x = 2 ** 32
    max_x = - 2 ** 32

    min_y = min_x
    max_y = max_x

    for coord in coords:
        min_x = min(min_x, coord[0])
        max_x = max(max_x, coord[0])

        min_y = min(min_y, coord[1])
        max_y = max(max_y, coord[1])

    print(max_x - min_x, max_y - min_y)


print(part2())
