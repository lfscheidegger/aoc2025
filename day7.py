from functools import cache
import sys

def part1():
    lines = [l.strip() for l in sys.stdin]

    count = 0

    for row in range(1, len(lines)):
        line = lines[row]
        for col in range(len(line)):
            if lines[row][col] == '^' and lines[row-1][col] == '|':
                # new split
                count += 1
                lines[row] = lines[row][:col - 1] + '|^|' + lines[row][col + 2:]
            elif lines[row - 1][col] == '|' or lines[row - 1][col] == 'S':
                # just move the beam down
                lines[row] = lines[row][:col] + '|' + lines[row][col + 1:]
            
    return count, lines


def part2():
    lines = part1()[1]

    @cache
    def n_timelines(row, col):
        assert(lines[row][col] == '|')
        
        if row == len(lines) - 1:
            # base case particle leaving bottom
            return 1
        elif lines[row + 1][col] == '|':
            # ray just keeps going down
            return n_timelines(row + 1, col)
        elif lines[row + 1][col] == '^':
            # actual split
            return n_timelines(row + 1, col - 1) + n_timelines(row + 1, col + 1)

    return n_timelines(1, len(lines[0]) // 2)

    

print(part2())
