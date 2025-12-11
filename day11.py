from collections import defaultdict
from functools import cache
import sys


def part1():
    nodes = set()
    edges = defaultdict(set)

    @cache
    def count(from_, to):
        if to in edges[from_]:
            return 1

        result = 0
        for node in edges[from_]:
            result += count(node, to)

        return result

    for line in sys.stdin:
        from_, tos = line.strip().split(":")
        for to in tos.strip().split():
            if to not in edges:
                edges[to] = set()

        for to in tos.strip().split():
            edges[from_].add(to)

            
    return count('you', 'out')


def part2():
    nodes = set()
    edges = defaultdict(set)

    @cache
    def count(from_, to, exclude = None):
        if exclude is None:
            exclude = frozenset()
            
        if to in exclude:
            return 0
        
        if to in edges[from_]:
            return 1

        result = 0
        for node in edges[from_]:
            if node in exclude:
                continue

            result += count(node, to, exclude)

        return result

    for line in sys.stdin:
        from_, tos = line.strip().split(":")
        if from_ not in nodes:
            nodes.add(from_)
    
        for to in tos.strip().split():
            if to not in edges:
                edges[to] = set()

        for to in tos.strip().split():
            edges[from_].add(to)

    result = 0

    # svr -> fft -> dac -> out    
    dac_to_out = count('dac', 'out', frozenset({'svr', 'fft'}))
    fft_to_dac = count('fft', 'dac', frozenset({'svr', 'out'}))
    svr_to_fft = count('svr', 'fft', frozenset({'dac', 'out'}))
    result += svr_to_fft * fft_to_dac * dac_to_out

    # svr -> dac -> fft -> out
    fft_to_out = count('fft', 'out', frozenset({'svr', 'dac'}))
    dac_to_fft = count('dac', 'fft', frozenset({'svr', 'out'}))
    svr_to_dac = count('svr', 'dac', frozenset({'fft', 'out'}))
    result += svr_to_dac * dac_to_fft * fft_to_out

    return result

    
print(part2())
        
