from collections import deque


FNAME = "./inp.txt"

with open(FNAME, "r") as f:
    data = f.read().strip()

# NBYTES = 1024
Point = tuple[int, int]
pts: set[Point] = set()

maxrow = 70
maxcol = 70

START = (0, 0)
END = (maxrow, maxcol)

dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

res = 0

for row in data.splitlines(False):
    x, y = row.split(",")
    new_p = (int(y), int(x))
    pts.add(new_p)

    q: deque[tuple[Point, int]] = deque([(START, 0)])
    seen = set()

    while q:
        p, n = q.popleft()
        if p in seen:
            continue
        seen.add(p)
        if p == END:
            res = n
            break
        for d in dirs:
            np = (p[0] + d[0], p[1] + d[1])
            if 0 <= np[0] <= maxrow and 0 <= np[1] <= maxcol and np not in pts:
                q.append((np, n + 1))
    else:
        for i in range(maxrow + 1):
            for j in range(maxcol + 1):
                p = (i, j)
                if p in pts:
                    print("#", end="")
                else:
                    print(".", end="")
            print()

        print(f"Res: {new_p[1]},{new_p[0]}")
        break
