from collections import defaultdict
from itertools import combinations

FNAME = "./inp.txt"

Point = tuple[int, int]

with open(FNAME, "r") as f:
    data = f.read()
lines = data.splitlines(keepends=False)


MAP: list[list[str]] = [list(l) for l in lines]

max_row = len(MAP) - 1
max_col = len(MAP[0]) - 1

antennas: defaultdict[str, set[Point]] = defaultdict(set)
antinodes: set[Point] = set()

for ridx, row in enumerate(lines):
    for cidx, col in enumerate(row):
        if col != ".":
            antennas[col].add((ridx, cidx))


def print_map():
    for ridx, row in enumerate(lines):
        for cidx, col in enumerate(row):
            if (ridx, cidx) in antinodes:
                print("#", end="")
            else:
                print(col, end="")
        print()


# type of antenna and locations of antennas for each type
for t, ants in antennas.items():
    for a, b in combinations(ants, 2):
        rdx = a[0] - b[0]
        cdx = a[1] - b[1]

        # points with directions
        ns = [(a, +1), (b, -1)]

        while ns:
            n, ds = ns.pop()
            if 0 <= n[0] <= max_row and 0 <= n[1] <= max_col:
                antinodes.add(n)
                # add new point, that goes along the same direction
                ns.append(((n[0] + rdx * ds, n[1] + cdx * ds), ds))

print_map()
print(len(antinodes))
