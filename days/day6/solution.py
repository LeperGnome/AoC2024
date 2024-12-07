from itertools import cycle
from copy import deepcopy
import operator
from typing import TypeVar

FNAME = "./inp.txt"

Point = tuple[int, int]


def add_points(p1: Point, p2: Point) -> Point:
    return tuple(map(operator.add, p1, p2))


T = TypeVar("T")


with open(FNAME, "r") as f:
    data = f.read()

lines = data.splitlines(keepends=False)

MAP: list[list[str]] = [list(l) for l in lines]
dirs = cycle([(-1, 0), (0, 1), (1, 0), (0, -1)])

max_row = len(MAP) - 1
max_col = len(MAP[0]) - 1


def get_guard_pos() -> Point:
    for ridx, row in enumerate(MAP):
        for cidx, col in enumerate(row):
            if col == "^":
                return ridx, cidx
    raise RuntimeError("didn't find the guard")


def is_leads_to_loop(ray_pos: Point, dirs_c, map_: list[list[str]]) -> bool:
    cells_c: set[tuple[Point, Point]] = set()

    # initial turn
    dir = next(dirs_c)

    while True:
        # i reach a point where i was before
        if (ray_pos, dir) in cells_c:
            return True

        cells_c.add((ray_pos, dir))
        next_pos = add_points(ray_pos, dir)

        row, col = next_pos

        # go out of bounds
        if row > max_row or col > max_col or row < 0 or col < 0:
            return False

        # turning
        if map_[row][col] == "#":
            dir = next(dirs_c)
            continue

        # walk in the same direction
        ray_pos = next_pos


guard_pos: Point = get_guard_pos()
pts: set[Point] = set()  # points, that i've visited
pts_loc: set[tuple[Point, Point]] = set()  # points, that i've visited (with location)
obst: set[Point] = set()  # valid obstacles, that lead to loops

cur_pos = guard_pos
cur_dir = next(dirs)


def print_map(cur: Point):
    for ridx, row in enumerate(MAP):
        for cidx, col in enumerate(row):
            p = (ridx, cidx)
            if p in obst:
                print("O", end="")
            elif p == cur:
                print("*", end="")
            elif p in pts:
                print("X", end="")
            else:
                print(col, end="")
        print()


while True:
    pts_loc.add((cur_pos, cur_dir))
    pts.add(cur_pos)

    next_pos = add_points(cur_pos, cur_dir)
    row, col = next_pos

    if row > max_row or col > max_col or row < 0 or col < 0:
        break

    # turning
    if MAP[row][col] == "#":
        cur_dir = next(dirs)
        continue

    # modifying map copy - putting an obstacle
    map_ = deepcopy(MAP)
    map_[row][col] = "#"
    if (
        next_pos not in pts  # can't block my way from the past
        and next_pos not in obst  # not a known obstacle
        and is_leads_to_loop(cur_pos, deepcopy(dirs), map_)  # adding it leads to a loop
    ):
        obst.add(next_pos)

    cur_pos = next_pos


print_map(cur_pos)
print(len(obst))
