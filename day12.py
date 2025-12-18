from dataclasses import dataclass
from typing import Generator, List, NewType, Tuple, Union
import sys


Present = NewType('Present', int)


@dataclass(frozen = True)
class Region:
    width: int
    data: List[int]

    @staticmethod
    def from_width_height(width: int, height: int) -> 'Region':
        return Region(width = width, data = [0] * height)

    def __repr__(self):
        result = ''
        for row in self.data:
            result += f'{row:0{self.width}b}'.replace('0', '.').replace('1', '#') + '\n'
        return result

    def try_fit(self, present: Present, offset: Tuple[int, int]) -> 'Region':
        """
        Try to fit the given present in the given region, with the optional given offset.
        The offset moves presents from top to bottom and *right to left*.

        Returns the new region, or same if it's not possible to fit."""
        if offset[0] + 3 > len(self.data):
            # hardcoded 3 because that's the height of a present and all presents in the input
            # fully need all 3 rows and columns
            return self
    
        result = list(self.data)
        for idx in range(3):
            region_row = result[offset[0] + idx]
            present_row = ((present >> 3 * (2 - idx)) & 7) << offset[1]

            if (present_row & region_row != 0) or present_row > 2 ** self.width - 1:
                # If there's overlap, the present doesn't fit
                return self
            result[offset[0] + idx] = present_row | region_row
    
        return Region(self.width, result)  


def shape_str_to_present(shape_str: str) -> Present:
    result = 0

    for idx, ch in enumerate(reversed(shape_str)):
        result += 2**idx if ch == '#' else 0

    assert result < 2**9
    return result


def present_to_shape_str(present: Present) -> str:
    result = ''
    while present > 0:
        result += '#' if present % 2 else '.'
        present //= 2

    result = '.' * (9 - len(result)) + ''.join(reversed(result))
    assert(len(result) == 9)
    return result


def shape_str_to_shape_str_array(shape_str: str) -> List[str]:
    assert(len(shape_str) == 9)

    return [shape_str[:3], shape_str[3:6], shape_str[6:9]]


def shape_str_array_to_shape_str(shape_str_array: List[str]) -> str:
    return shape_str_array[0] + shape_str_array[1] + shape_str_array[2]


def variants(present: Present) -> Generator[Present]:
    shape_str_array = shape_str_to_shape_str_array(present_to_shape_str(present))

    # horizontal flip
    temp = list(shape_str_array)
    
    temp[0] = shape_str_array[0][2] + shape_str_array[0][1] + shape_str_array[0][0]
    temp[1] = shape_str_array[1][2] + shape_str_array[1][1] + shape_str_array[1][0]
    temp[2] = shape_str_array[2][2] + shape_str_array[2][1] + shape_str_array[2][0]

    yield shape_str_to_present(shape_str_array_to_shape_str(temp))
    
    # vertical flip
    yield shape_str_to_present(shape_str_array_to_shape_str([
        shape_str_array[2],
        shape_str_array[1],
        shape_str_array[0]]))

    # 90 deg. rotation
    temp = [[shape_str_array[2][0], shape_str_array[1][0], shape_str_array[0][0]],
            [shape_str_array[2][1], shape_str_array[1][1], shape_str_array[0][1]],
            [shape_str_array[2][2], shape_str_array[1][2], shape_str_array[0][2]]]
    yield shape_str_to_present(shape_str_array_to_shape_str(temp))

    # 180 deg. rotation
    temp = [[shape_str_array[2][2], shape_str_array[2][1], shape_str_array[2][0]],
            [shape_str_array[1][2], shape_str_array[1][1], shape_str_array[1][0]],
            [shape_str_array[0][2], shape_str_array[0][1], shape_str_array[0][0]]]
    yield shape_str_to_present(shape_str_array_to_shape_str(temp))

    # 270 deg rotation
    temp = [[shape_str_array[0][2], shape_str_array[1][2], shape_str_array[2][2]],
            [shape_str_array[0][1], shape_str_array[1][1], shape_str_array[2][1]],
            [shape_str_array[0][0], shape_str_array[1][0], shape_str_array[2][0]]]
    yield shape_str_to_present(shape_str_array_to_shape_str(temp))


def print_present(present: Union[Present, str, List[str]]):
    shape_str_array = []
    if isinstance(present, int):
        shape_str_array = shape_str_to_shape_str_array(present_to_shape_str(present))
    elif isinstance(present, str):
        shape_str_array = shape_str_to_shape_str_array(present)
    else:
        shape_str_array = present

    for s in shape_str_array:
        print(s)


def parse_input():
    presents = []
    goal_states = []
    latest_shape_strs = []
    for line in sys.stdin:
        line = line.strip()
        if 'x' in line:
            left, right = line.split(':')
            width, height = left.strip().split('x')

            present_counts = [int(x) for x in right.strip().split()]
            goal_states.append((Region.from_width_height(int(width), int(height)), present_counts))

        elif line == '':
            presents.append(shape_str_to_present(shape_str_array_to_shape_str(latest_shape_strs)))
            latest_shape_strs = []

        elif ':' in line:
            continue

        else:
            latest_shape_strs.append(line.strip())

    return (presents, goal_states)
            

def part1():
    data = parse_input()

    


print(part1())
