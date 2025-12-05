import sys

def part1():
    def get_joltage(bank: str):
        bank = bank.strip()
        left = max(bank[:-1])
        idx = bank.find(left)
        right = max(bank[idx+1:])

        return int(f'{left}{right}')

    result = 0
    for line in sys.stdin:
        result += get_joltage(line)

    print(result)


def part2():
    def get_joltage_head(bank: str, how_many: int):
        head = max(bank[:-how_many])
        return head, bank.find(head)


    def get_joltage(bank: str):
        bank = bank.strip()
        joltage_str = ""
        for how_many in range(11, 0, -1):
            head, cutoff = get_joltage_head(bank, how_many)
            joltage_str += head
            bank = bank[cutoff+1:]

        joltage_str += max(bank)
        return int(joltage_str)

    result = 0
    for line in sys.stdin:
        result += get_joltage(line)

    print(result)
    

part2()
