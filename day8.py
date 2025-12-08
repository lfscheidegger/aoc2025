from collections import defaultdict

import dataclasses
import itertools
import sys


@dataclasses.dataclass
class Junction:
    idx: int
    x: int
    y: int
    z: int


def part1():    
    lines = [l.strip().split(',') for l in sys.stdin]
    junctions = [Junction(idx, int(x), int(y), int(z)) for idx, (x, y, z) in enumerate(lines)]

    distances = []
    for i in range(len(junctions)):
        for j in range(i+1, len(junctions)):
            left = junctions[i]
            right = junctions[j]

            distances.append((
                (i, j),
                (left.x - right.x) ** 2 + (left.y - right.y) ** 2 + (left.z - right.z) ** 2))

    distances.sort(key= lambda d: d[1])

    circuits = { idx: idx for idx in range(len(junctions)) }

    remaining_to_connect = 1000

    for distance in distances:
        (left, right), value = distance

        to_connect = min(circuits[left], circuits[right])
        from_connect = max(circuits[left], circuits[right])
        for idx in circuits.keys():
            if circuits[idx] == from_connect:
                circuits[idx] = to_connect
        
        remaining_to_connect -= 1

        if not remaining_to_connect:
            break

    sizes = defaultdict(int)
    for circuit_idx, junction_idx in circuits.items():
        sizes[junction_idx] += 1

    sizes = list(sizes.values())
    sizes.sort(key=lambda x: -x)
    print(sizes)

    return (sizes[0]) * (sizes[1]) * (sizes[2])


def part2():
    lines = [l.strip().split(',') for l in sys.stdin]
    junctions = [Junction(idx, int(x), int(y), int(z)) for idx, (x, y, z) in enumerate(lines)]

    distances = []
    for i in range(len(junctions)):
        for j in range(i+1, len(junctions)):
            left = junctions[i]
            right = junctions[j]

            distances.append((
                (i, j),
                (left.x - right.x) ** 2 + (left.y - right.y) ** 2 + (left.z - right.z) ** 2))

    distances.sort(key= lambda d: d[1])

    circuits = { idx: idx for idx in range(len(junctions)) }

    circuit_count = len(circuits)

    for distance in distances:
        (left, right), _ = distance

        to_connect = min(circuits[left], circuits[right])
        from_connect = max(circuits[left], circuits[right])

        if to_connect == from_connect:
            continue

        for idx in circuits.keys():
            if circuits[idx] == from_connect:
                circuits[idx] = to_connect

        circuit_count -= 1
        if circuit_count == 1:
            return junctions[left].x * junctions[right].x


print(part2())
