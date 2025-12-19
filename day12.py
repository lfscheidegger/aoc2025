from dataclasses import dataclass
from functools import cache
from typing import Generator, List, NewType, Tuple, Union
import sys


"""
Encodes a 3x3 binary grid in the 9 least significant bits, followed by 6 bits of horizontal offset and 6 bits of vertical offset
"""
Present = NewType('Present', int)


@dataclass(frozen = True)
class Region:
    width: int
    data: Tuple[int]
    area: int

    @staticmethod
    def from_width_height(width: int, height: int) -> 'Region':
        return Region(width = width, data = tuple([0] * height), area = width * height)

    def __repr__(self):
        result = ''
        for row in self.data:
            result += f'{row:0{self.width}b}'.replace('0', '.').replace('1', '#') + '\n'
        return result

    def try_fit(self, present: Present) -> 'Region':
        """
        Try to fit the given present in the given region, with the optional given offset.
        The offset moves presents from top to bottom and *right to left*.

        Returns the new region, or same if it's not possible to fit."""
        if present_area(present) > self.area:
            return self
        
        offset = (present >> 15) & (2**6 - 1), (present >> 9) & (2**6 - 1)
        present &= 511
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
    
        return Region(self.width, tuple(result), self.area - present_area(present))


def shape_str_to_present(shape_str: str) -> Present:
    result = 0

    for idx, ch in enumerate(reversed(shape_str)):
        result += 2**idx if ch == '#' else 0

    assert result < 2**9
    return result


def present_to_shape_str(present: Present) -> str:
    result = ''
    present &= 511
    while present > 0:
        result += '#' if present % 2 else '.'
        present >>= 1

    result = '.' * (9 - len(result)) + ''.join(reversed(result))
    assert(len(result) == 9)
    return result


@cache
def present_area(present: Present) -> int:
    result = 0
    present &= 511
    while present > 0:
        result += 1 if present % 2 else 0
        present >>= 1

    return result


def shape_str_to_shape_str_array(shape_str: str) -> List[str]:
    assert(len(shape_str) == 9)

    return [shape_str[:3], shape_str[3:6], shape_str[6:9]]


def shape_str_array_to_shape_str(shape_str_array: List[str]) -> str:
    return shape_str_array[0] + shape_str_array[1] + shape_str_array[2]


def region_variants(present: Present, region: Region) -> Generator[Present]:
    assert(present < 512)

    for x in range(region.width - 2):
        for y in range(len(region.data) - 2):
            yield (y << 15) | (x << 9) | present

def variants(present: Present, region: Region) -> Generator[Present]:
    assert(present < 512)

    unique_presents = set()
    unique_presents.add(present)
    
    shape_str_array = shape_str_to_shape_str_array(present_to_shape_str(present))

    # horizontal flip
    temp = list(shape_str_array)
    temp[0] = shape_str_array[0][2] + shape_str_array[0][1] + shape_str_array[0][0]
    temp[1] = shape_str_array[1][2] + shape_str_array[1][1] + shape_str_array[1][0]
    temp[2] = shape_str_array[2][2] + shape_str_array[2][1] + shape_str_array[2][0]

    unique_presents.add(shape_str_to_present(shape_str_array_to_shape_str(temp)))
    
    # vertical flip
    unique_presents.add(shape_str_to_present(shape_str_array_to_shape_str([
        shape_str_array[2],
        shape_str_array[1],
        shape_str_array[0]])))

    # 90 deg. rotation
    temp = [[shape_str_array[2][0], shape_str_array[1][0], shape_str_array[0][0]],
            [shape_str_array[2][1], shape_str_array[1][1], shape_str_array[0][1]],
            [shape_str_array[2][2], shape_str_array[1][2], shape_str_array[0][2]]]
    unique_presents.add(shape_str_to_present(shape_str_array_to_shape_str(temp)))

    # 180 deg. rotation
    temp = [[shape_str_array[2][2], shape_str_array[2][1], shape_str_array[2][0]],
            [shape_str_array[1][2], shape_str_array[1][1], shape_str_array[1][0]],
            [shape_str_array[0][2], shape_str_array[0][1], shape_str_array[0][0]]]
    unique_presents.add(shape_str_to_present(shape_str_array_to_shape_str(temp)))

    # 270 deg rotation
    temp = [[shape_str_array[0][2], shape_str_array[1][2], shape_str_array[2][2]],
            [shape_str_array[0][1], shape_str_array[1][1], shape_str_array[2][1]],
            [shape_str_array[0][0], shape_str_array[1][0], shape_str_array[2][0]]]
    unique_presents.add(shape_str_to_present(shape_str_array_to_shape_str(temp)))

    for present_shape in unique_presents:
        for p in region_variants(present_shape, region):
            yield p


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

    if isinstance(present, int):
        x_offset = (present >> 9) & (2**6 - 1)
        y_offset = (present >> 15) & (2**6 - 1)
        print(f'{x_offset}x{y_offset}')


def parse_input():
    presents = []
    goal_states = []
    latest_shape_strs = []
    for line in sys.stdin:
        line = line.strip()
        if 'x' in line:
            left, right = line.split(':')
            width, height = left.strip().split('x')

            present_counts = tuple([int(x) for x in right.strip().split()])
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
    """
    data = parse_input()

    def can_fit(presents: Tuple[Present], goal_state: Tuple[Region, List[int]]) -> bool:
        region, desired_presents = goal_state

        # print(region, desired_presents)

        if sum(desired_presents) == 0:
            return True

        # first non-zero present
        present_idx = list(filter(lambda g: g[1] != 0, enumerate(desired_presents)))[0][0]

        goal_state_without_present = tuple(
            p - 1
            if idx == present_idx
            else p for (idx, p) in enumerate(desired_presents))


        total_desired_area = sum([present_area(presents[idx]) * count for idx, count in enumerate(desired_presents)])
        if total_desired_area > region.area:
            # not enough room left, no need to bother trying
            return False
        
        present = presents[present_idx]

        for variant in variants(present, region):
            with_fit = region.try_fit(variant)
            # print(with_fit)
            if with_fit.data == region.data:
                # This variant doesn't fit
                continue
            else:
                # This variant of the present fits
                if can_fit(presents, (with_fit, goal_state_without_present)):
                    # And all others fit
                    return True
                else:
                    # Strictly not needed, but indicates that we need to try another variant
                    continue

        # No variant of this present fits, so cut short
        return False

    result = 0
    presents = tuple(data[0])

    for goal_state in data[1]:
        if can_fit(presents, goal_state):
            result += 1

    return result
    """

    data = parse_input()
    presents = data[0]

    result = 0
    for goal_state in data[1]:
        region, desired_presents = goal_state
        total_desired_area = sum([present_area(presents[idx]) * count for idx, count in enumerate(desired_presents)])
        if total_desired_area <= region.area:
            result += 1

    return result
    

print(part1())
