from collections import defaultdict
from copy import deepcopy


FNAME = "./inp.txt"

with open(FNAME, "r") as f:
    data = f.read()

lines = data.splitlines(keepends=False)

should_come_after = defaultdict(set)
should_come_before = defaultdict(set)
updates: list[list[int]] = []

in_rules = True
for l in lines:
    if l == "":
        in_rules = False
        continue

    if in_rules:
        k, v = l.split("|", 1)
        k = int(k)
        v = int(v)
        should_come_after[k].add(v)
        should_come_before[v].add(k)
    else:
        updates.append(list(map(int, l.split(","))))

res = 0

for idx, upd in enumerate(updates):
    found = False
    broke = False
    upd = deepcopy(upd)
    while not found:
        before, after = {upd[0]}, set(upd[1:])

        for widx, page in enumerate(upd[1:]):
            after.remove(page)

            pidx = widx + 1  # because using upd[1:]

            # breaking rules
            bta = (
                before & should_come_after[page]
            )  # should be moved from before to after
            atb = (
                after & should_come_before[page]
            )  # should be moved from after to before

            for el in bta | atb:
                eidx = upd.index(el)
                upd[eidx], upd[pidx] = upd[pidx], upd[eidx]

            if bta | atb:
                broke = True
                break

            before.add(page)
        else:
            found = True
            if broke:
                res += upd[int(len(upd) / 2)]

print(res)
