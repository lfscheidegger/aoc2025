from dataclasses import dataclass
import sys


@dataclass(frozen=False)
class Interval:
    left: int
    right: int

    def __post_init__(self):
        if self.left > self.right:
            raise ValueError("Left bound must be less than or equal to right bound")

    def contains(self, candidate: Union[int, 'Interval']) -> bool:
        if isinstance(candidate, int):
            return self.left <= candidate < self.right

        if candidate.is_empty():
            return True

        return candidate.left >= self.left and candidate.right <= self.right

    def is_empty(self) -> bool:
        return self.right - self.left == 1


def union(intervals: List[Interval]) -> List[Interval]:
    if not intervals:
        return []
    sorted_intervals = sorted(intervals, key=lambda x: x.left)
    merged = [sorted_intervals[0]]
    for current in sorted_intervals[1:]:
        last = merged[-1]
        if current.left <= last.right:
            last.right = max(last.right, current.right)
        else:
            merged.append(current)
    return merged    

    
def part1():
    ranges = []
    found_break = False
    result =0 
    for line in sys.stdin:        
        if line == "\n":
            found_break = True
            continue
        if not found_break:
            min, max = line.split("-")
            min = int(min)
            max = int(max)
            ranges.append([min, max])
        else:
            test = int(line)
            for range_ in ranges:
                if test >= range_[0] and test <= range_[1]:
                    print(test, "fresh")
                    result += 1
                    break
            pass
        pass

    return result


def part2():
    intervals = []
    for line in sys.stdin:        
        min, max = line.split("-")
        next_interval = Interval(int(min), int(max))

        intervals = union(intervals + [next_interval])

    result = 0
    for interval in intervals:
        result += interval.right - interval.left + 1

    return result


print(part2())
