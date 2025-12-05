import sys

def part1():
    grid = []
    result = 0
    for line in sys.stdin:
        grid.append(line.strip())

    height = len(grid)
    width = len(grid[0])

    for y in range(0, len(grid)):
        for x in range(0, len(grid[y])):
            if grid[y][x] != '@':
                continue


            tl = grid[y-1][x-1] if x > 0 and y > 0 else '.'
            t = grid[y-1][x] if y > 0 else '.'            
            tr = grid[y-1][x+1] if x < width -1 and y > 0 else '.'
            l = grid[y][x-1] if x > 0 else '.'            
            r = grid[y][x+1] if x < width - 1 else '.'
            bl = grid[y+1][x-1] if x > 0 and y < height - 1 else '.'
            b = grid[y+1][x] if y < height -1 else '.'
            br = grid[y+1][x+1] if x < width - 1 and y < height -1 else '.'

            total = sum(map(lambda entry: 1 if entry == '@' else 0, [tl, t, tr, l, r, bl, b, br]))
            if total < 4:
                result += 1

    return result
                


def part2():
    def get_grid():
        grid = []
        for line in sys.stdin:
            grid.append(line.strip())

        return grid

    grid = get_grid()
    height = len(grid)
    width = len(grid[0])    
    
    def single(grid, count):
        for y in range(0, len(grid)):
            for x in range(0, len(grid[y])):
                if grid[y][x] != '@':
                    continue

                tl = grid[y-1][x-1] if x > 0 and y > 0 else '.'
                t = grid[y-1][x] if y > 0 else '.'            
                tr = grid[y-1][x+1] if x < width -1 and y > 0 else '.'
                l = grid[y][x-1] if x > 0 else '.'            
                r = grid[y][x+1] if x < width - 1 else '.'
                bl = grid[y+1][x-1] if x > 0 and y < height - 1 else '.'
                b = grid[y+1][x] if y < height -1 else '.'
                br = grid[y+1][x+1] if x < width - 1 and y < height -1 else '.'

                total = sum(map(lambda entry: 1 if entry == '@' else 0, [tl, t, tr, l, r, bl, b, br]))
                if total < 4:
                    grid[y] = f'{grid[y][:x]}.{grid[y][x+1:]}'

                    return grid, count + 1

        return grid, None

    count = 0
    final_count = -1
    while count != None:
        grid, count = single(grid, count)
        final_count = count if count is not None else final_count

    return final_count

print(part2())
