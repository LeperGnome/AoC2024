from uuid import UUID, uuid4
from typing import NamedTuple
from collections import deque
from dataclasses import dataclass

FNAME = "./inp.txt"

with open(FNAME, "r") as f:
    data = f.read().strip()

Point = tuple[int, int]


class RegID(NamedTuple):
    char: str
    idx: UUID


@dataclass
class RegInfo:
    perimeter: int
    area: int
    sides: int


MAP: list[list[str]] = [list(l) for l in data.splitlines(False)]
max_row = len(MAP) - 1
max_col = len(MAP[0]) - 1

DIRS: list[Point] = [(-1, 0), (0, 1), (1, 0), (0, -1)]


REGIONS: dict[RegID, RegInfo] = {}
SEEN: set[Point] = set()
POINTS_TO_REGION: dict[Point, RegID] = {}


# determining regions
for ridx, row in enumerate(MAP):
    for cidx, char in enumerate(row):
        p = (ridx, cidx)
        if p in SEEN:
            continue
        SEEN.add(p)

        region_cells = set()
        perimeter = 0
        q = deque([p])

        while q:
            cell = q.popleft()
            if cell in region_cells:
                continue

            region_cells.add(cell)
            SEEN.add(cell)

            for d in DIRS:
                ncell = (cell[0] + d[0], cell[1] + d[1])
                if (
                    0 <= ncell[0] <= max_row
                    and 0 <= ncell[1] <= max_col
                    and MAP[ncell[0]][ncell[1]] == char
                ):
                    q.append(ncell)
                else:
                    perimeter += 1

        reg_id = RegID(char=char, idx=uuid4())
        REGIONS[reg_id] = RegInfo(perimeter=perimeter, area=len(region_cells), sides=0)
        for pt in region_cells:
            POINTS_TO_REGION[pt] = reg_id


# calculating horizontal edges
for ridx, row in enumerate(MAP):
    for dside in [-1, 1]:  # for top and bottom edge
        prev = None
        for cidx, char in enumerate(row):
            is_edge = bool(
                ridx + dside > max_row
                or ridx + dside < 0
                or MAP[ridx + dside][cidx] != char
            )

            # initial edge start
            if is_edge and prev is None:
                prev = char
                continue

            # finished the edge
            if prev is not None and (not is_edge or prev != char):
                reg_id = POINTS_TO_REGION[(ridx, cidx - 1)]
                REGIONS[reg_id].sides += 1

                # started a new edge
                if is_edge:
                    prev = char
                else:
                    prev = None

        if prev:
            reg_id = POINTS_TO_REGION[(ridx, max_col)]
            REGIONS[reg_id].sides += 1


# calculating vertical edges
for cidx in range(max_col + 1):
    for dside in [-1, 1]:  # for left and right edges
        prev = None
        for ridx in range(max_row + 1):
            char = MAP[ridx][cidx]

            is_edge = bool(
                cidx + dside > max_col
                or cidx + dside < 0
                or MAP[ridx][cidx + dside] != char
            )
            if is_edge:
                print(char, is_edge)

            # initial edge start
            if is_edge and prev is None:
                prev = char
                continue

            # finished the edge
            if prev is not None and (not is_edge or prev != char):
                reg_id = POINTS_TO_REGION[(ridx - 1, cidx)]
                REGIONS[reg_id].sides += 1

                # started a new edge
                if is_edge:
                    prev = char
                else:
                    prev = None

        if prev:
            reg_id = POINTS_TO_REGION[(max_row, cidx)]
            REGIONS[reg_id].sides += 1


for rid, rinfo in REGIONS.items():
    print(f"{rid.char}: {rinfo.area=} {rinfo.perimeter=} {rinfo.sides=}")

price = sum(r.sides * r.area for r in REGIONS.values())
print(price)
