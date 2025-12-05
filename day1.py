import sys

def part1():
    value = 50
    result = 0
    for line in sys.stdin:
        next_value = int(line.replace("L", "-").replace("R", "+"))
        value += next_value
        if value % 100 == 0:
            result += 1

    print(result)

def part2():
    value = 50
    result = 0
    previous_was_zero = False
    print(value, 0, result)
    for line in sys.stdin:
        movement = int(line.replace("L", "-").replace("R", "+"))

        while abs(movement) >= 100:
            if movement < 0:
                movement += 100
            else:
                movement -= 100
            result += 1

        value += movement
        if value >= 100:
            value %= 100
            result += 1
        elif value < 0:
            if value - movement != 0:
                result  += 1            
            value %= 100
        elif value == 0:
            result += 1

        print(value, movement, result)

    print()
    print(result)

part2()
        
