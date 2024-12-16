from contextlib import contextmanager
from heapq import heappop, heappush
from dataclasses import dataclass, field

FNAME = "./inp.txt"

with open(FNAME, "r") as f:
    data = f.read().strip()

MAP: list[list[str]] = [list(l) for l in data.splitlines(False)]
max_row = len(MAP) - 1
max_col = len(MAP[0]) - 1
Point = tuple[int, int]


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


@dataclass(order=True)
class Pos:
    pt: Point = field(compare=False)
    d: Point = field(compare=False)
    score: int
    hist: set[Point]


def print_map(seen, on_best_path):
    for ri, row in enumerate(MAP):
        for ci, col in enumerate(row):
            p = (ri, ci)
            if p in on_best_path:
                print("O", end="")
            elif p in seen:
                print("*", end="")
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

lptscore = {}


def solution():
    q: list[Pos] = [Pos(pt=START, d=dirs[0], score=0, hist=set())]
    best_score = float("inf")
    on_best_path: set[Point] = {START}
    seen = set()

    while q:
        with alt_buffer():
            print_map(seen, on_best_path)
            input()

        pos = heappop(q)

        ls = lptscore.get((pos.pt, pos.d), None)
        if ls and pos.score > ls:
            continue
        else:
            lptscore[(pos.pt, pos.d)] = pos.score

        if pos.score > best_score:
            break

        seen.add(pos.pt)

        if pos.pt == END:
            best_score = pos.score
            on_best_path |= pos.hist

        for d in dirs:
            npt = add_points(pos.pt, d)
            if 0 <= npt[0] <= max_row and 0 <= npt[1] <= max_col and map_at(npt) != "#":
                heappush(
                    q,
                    Pos(
                        pt=npt,
                        d=d,
                        score=pos.score + 1 + 1000 * int(d != pos.d),
                        hist=pos.hist | {npt},
                    ),
                )
    return best_score, on_best_path


score, on_best = solution()
print(score, len(on_best))
