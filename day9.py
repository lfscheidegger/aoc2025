from collections import defaultdict
from dataclasses import dataclass
from typing import Generator, List, Tuple
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


def input_to_svg():
    lines = list(sys.stdin)
    print("""<svg width="1000" height="1000" xmlns="http://www.w3.org/2000/svg">""")

    path_string = """<path stroke-width="0.1" stroke="black" fill="transparent" marker-start="url(#dot)" marker-mid="url(#dot)" marker-end="url(#dot)" d="M """

    x, y = lines[0].split(",")
    path_string += f"{int(x) / 100} {int(y) / 100}"
    lines = lines[1:]

    for line in lines:
        x, y = line.split(",")
        x, y = int(x), int(y)
        path_string += f" L {x / 100} {y / 100}"
        

    path_string += "\" />"

    print(path_string)
    
    print("""</svg>""")


def part2():
    """
    This doesn't solve the general case but the actual shape is like a backwards pacman."""
    coords = [(int(x), int(y)) for x, y in [l.strip().split(",") for l in sys.stdin]]

    # The two "extreme points" to consider are one that's furthest right from its previous
    # neighbor and then the one right after it
    max_x_distance = max(enumerate(map(lambda c: c[1][0] - c[0][0], zip(coords, coords[1:]))), key=lambda v: v[1])
    extremum_idx = max_x_distance[0] + 1
    other_extremum_idx = extremum_idx + 1

    rightest_x = coords[extremum_idx][0]

    lowest_y = 0
    # The len(coords) // 2 bullshit is to make sure I only look at points "late enough" in the circle
    for neighbor, point in zip(coords[len(coords) // 2 + 1:], coords[len(coords) // 2:]):
        if neighbor[0] > rightest_x and point[0] < rightest_x:
            lowest_y = point[1]
            break

    bottom_left = None
    for thing in enumerate(zip(coords[1:], coords)):
        idx, (neighbor, point) = thing
        if neighbor[1] < lowest_y and point[1] > lowest_y:
            # The actual point is one prior to the point
            bottom_left = coords[idx + 1 - 2]


    top_right = coords[other_extremum_idx]
    print(top_right, bottom_left)

    return (1 + top_right[0] - bottom_left[0]) * (1 + top_right[1] - bottom_left[1])
    
    # This is the "top half" rectangle, which appears to be the wrong one
    #highest_y = 0
    #for neighbor, point in zip(coords[1:], coords):
    #    if neighbor[0] < rightest_x and point[0] > rightest_x:
    #        highest_y = point[1]
    #        break
    
    #top_left = None
    #for thing in enumerate(zip(coords[1:], coords)):
    #    idx, (neighbor, point) = thing
    #    if neighbor[1] < highest_y and point[1] > highest_y:
    #        top_left = coords[idx + 2]
    #        break

    #bottom_right = coords[extremum_idx]

    #print(top_left, bottom_right)
    #return (1 + bottom_right[0] - top_left[0]) * (1 + top_left[1] - bottom_right[1])


print(part2())




