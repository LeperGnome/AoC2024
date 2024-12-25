from collections import deque, defaultdict
from functools import reduce
from contextlib import contextmanager

FNAME = "./inp.txt"

with open(FNAME, "r") as f:
    data = f.read().strip()

MAP: list[list[str]] = [list(l) for l in data.splitlines(False)]
max_row = len(MAP) - 1
max_col = len(MAP[0]) - 1
Point = tuple[int, int]

class bcolors:
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

def get_coords(c: str) -> list[Point]:
    res = []
    for ri, row in enumerate(MAP):
        for ci, col in enumerate(row):
            if col == c:
                res.append((ri, ci))
    return res


def map_at(p: Point) -> str:
    return MAP[p[0]][p[1]]


def add_points(p1: Point, p2: Point) -> Point:
    return (p1[0] + p2[0], p1[1] + p2[1])

max_cheat_turns = 20 -1

def print_map(seen):
    for ri, row in enumerate(MAP):
        for ci, col in enumerate(row):
            p = (ri, ci)
            if p in seen:
                print(f"{bcolors.OKBLUE}*{bcolors.ENDC}", end="")
            else:
                print(col, end="")
        print()
    print()


@contextmanager
def alt_buffer():
    try:
        print("\033[?1049h\033[22;0;0t\033[0;0H", end="")
        yield
    finally:
        print("\033[?1049l\033[23;0;0t", end="")



START = get_coords("S")[0]
END = get_coords("E")[0]
dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def find_shortest_path() -> tuple[int, dict[Point, int]]:
    q = deque([(START, 0)])
    path_took = {}
    seen: set[Point] = set()
    while q:
        pt, l = q.popleft()
        if pt in seen:
            continue

        path_took[pt] = l
        seen.add(pt)
        if pt == END:
            print_map(seen)
            return l, path_took

        for d in dirs:
            np = add_points(pt, d)
            if (
                0 <= np[0] <= max_row and
                0 <= np[1] <= max_col and
                map_at(np) != "#"
            ):
                q.append((np, l+1))
    return -1, path_took

should_be_saved = 100

def get_cheat_exits(p: Point) -> set[Point]:
    exits = set()
    for i in range((-max_cheat_turns), max_cheat_turns+1):
        for j in range((-max_cheat_turns), max_cheat_turns+1):
            ex = add_points(p, (i, j))
            if (
                abs(i) + abs(j) <= max_cheat_turns 
                and 0 <= ex[0] <= max_row
                and 0 <= ex[1] <= max_col
                and map_at(ex) != "#"
            ):
                exits.add(ex)
    return exits


seen_cheats = set()
def saved_count() -> dict[int, set[tuple[Point, Point]]]:
    _, pt_to_took = find_shortest_path()
    res = defaultdict(set)
    for pt, took in pt_to_took.items():
        for d in dirs:
            # print(f"{pt=} {d=}   {res}")
            np = add_points(pt, d)
            if (
                0 <= np[0] <= max_row and
                0 <= np[1] <= max_col and
                map_at(np) == "#"
            ):
                exits = get_cheat_exits(np)
                for ex in exits:
                    ntook = abs(ex[0] - pt[0]) + abs(ex[1] - pt[1]) + took

                    if (bt := pt_to_took[ex] - ntook) >= should_be_saved:
                        seen_cheats.add((pt,ex))
                        res[bt].add((pt, ex))
                        continue

    return res

res = saved_count()
filtered = {k: v for k, v in res.items() if k >= should_be_saved}
print(filtered)
print(len(seen_cheats))

# 1086647 - too hight
# 960765 - too low
