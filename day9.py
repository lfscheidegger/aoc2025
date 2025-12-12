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


@dataclass(frozen=True)
class Segment:
    # x0, y0, x1, y1
    data: Tuple[int, int, int, int]

    @staticmethod
    def from_tuple(data: Tuple[int, int, int, int]) -> 'Segment':
        assert((data[0] == data[2]) or (data[1] == data[3]))
        return Segment((
            min(data[0], data[2]),
            min(data[1], data[3]),
            max(data[0], data[2]),
            max(data[1], data[3])))

    def __post_init__(self):
        x0, y0, x1, y1 = self.data
        if x0 != x1 and y0 != y1:
            raise ValueError("Segment must be horizontal or vertical")

        if x0 > x1 or y0 > y1:
            raise ValueError("Segment in wrong order")

    def direction(self) -> str:
        if self.data[0] == self.data[2]:
            return 'v'
        return 'h'

    def points(self) -> Generator[Tuple[int, int]]:
        if self.direction() == 'v':
            for y in range(self.data[1], self.data[3] + 1):
                yield self.data[0], y
        else:
            for x in range(self.data[0], self.data[2] + 1):
                yield x, self.data[1]

    def contains_point(self, p: Tuple[int, int]) -> bool:
        return p in self.points()

    def ray_crosses(self, p: Tuple[int, int]) -> str:
        """
        Whether a ray starting at p inclusive, going to positive horizontal infinity, crosses this
        segment. Returns n if the ray doesn't cross, y if it crosses, and i if the point is contained in
        the segment."""
        if self.contains_point(p):
            return 'i'

        if self.direction() == 'h':
            # Collinear to the ray
            return False

        point_is_to_the_left = p[0] < self.data[0]
        point_is_in_y_range = p[1] >= self.data[1] and p[1] <= self.data[3]

        return 'y' if point_is_to_the_left and point_is_in_y_range else 'n'

@dataclass(frozen = True)
class Box:
    data: Tuple[int, int, int, int]

    def __post_init__(self):
        x0, y0, x1, y1 = self.data

        if x0 > x1 or y0 > y1:
            raise ValueError("Segment in wrong order")

    def subdivide(self) -> Generator['Box']:
        x0, y0, x1, y1 = self.data
        
        if x0 == x1 and y0 == y1:
            raise ValueError('1x1 box cant be subdivided')

        split_x = (x0 + x1) // 2
        split_y = (y0 + y1) // 2

        yield Box(x0, y0, split_x, split_y)
        yield Box(split_x, y0, x1, split_y)
        # yield Box(x0, split_y, split_x, 


@dataclass(frozen = True)
class Polygon:
    segments: List[Segment]

    @staticmethod
    def from_input() -> 'Polygon':
        lines = list(sys.stdin)
        min_x, min_y = 2 ** 32, 2 ** 32
        max_x, max_y = -2 ** 32, -2 ** 32
        for line in lines:
            x, y = line.split(",")
            min_x = min(min_x, int(x))
            min_y = min(min_y, int(y))

            max_x = max(max_x, int(x))
            max_y = max(max_y, int(y))
        
        lines = lines + [lines[0]]

        segments = []
        for p1, p2 in zip(lines, lines[1:]):
            x, y = p1.split(",")
            p1 = (int(x) - min_x, int(y) - min_y)
            x, y = p2.split(",")
            p2 = (int(x) - min_x, int(y) - min_y)
            segments.append(Segment.from_tuple((p1[0], p1[1], p2[0], p2[1])))

        return Polygon(segments)
            
    def contains(p: Tuple[int, int]) -> True:
        """
        Returns true iff the given point is inside the given polygon. Points on the edge
        of the polygon count as inside."""
        n_crosses = 0
        for segment in self.segments:
            crosses = segment.ray_crosses(p)
            if crosses == 'i':
                return True
            elif crosses == 'y':
                n_crosses += 1
        return n_crosses % 2 == 1

def part2():
    p = Polygon.from_input()
    
    #coords = [(int(x), int(y)) for x, y in [l.strip().split(",") for l in sys.stdin]]

    #min_x = 2 ** 32
    #max_x = - 2 ** 32

    #min_y = min_x
    #max_y = max_x

    #for coord in coords:
    #    min_x = min(min_x, coord[0])
    #    max_x = max(max_x, coord[0])

    #    min_y = min(min_y, coord[1])
    #    max_y = max(max_y, coord[1])

    #print(max_x - min_x, max_y - min_y)


print(part2())


