FNAME = "./inp.txt"

with open(FNAME, "r") as f:
    data = f.read().strip()

Point = tuple[int, int]
MAP: list[list[int]] = [list(map(int, l)) for l in data.splitlines(False)]
DIRS: list[Point] = [(0, 1), (1, 0), (-1, 0), (0, -1)]

_map_max_row: int = len(MAP) - 1
_map_max_col: int = len(MAP[0]) - 1

trailheads: list[Point] = []
scores: dict[Point, int] = {}


for ridx, row in enumerate(MAP):
    for cidx, col in enumerate(row):
        if col == 0:
            trailheads.append((ridx, cidx))


def get_next_points(p: Point) -> list[Point]:
    res = []
    for d in DIRS:
        n = (p[0] + d[0], p[1] + d[1])
        if 0 <= n[0] <= _map_max_row and 0 <= n[1] <= _map_max_col:
            res.append(n)
    return res


q: list[Point] = trailheads
score = 0

while q:
    p = q.pop()

    val = MAP[p[0]][p[1]]

    # reached the peak
    if val == 9:
        score += 1

    next_points = get_next_points(p)
    for np in next_points:
        nval = MAP[np[0]][np[1]]
        if nval - val == 1:
            q.append(np)

print(score)
