from copy import deepcopy

FNAME = "./inp.txt"

with open(FNAME, "r") as f:
    lines = [[int(x) for x in l.strip().split(sep=" ")] for l in f.readlines()]

safe_cnt = {}
lines_orig = deepcopy(lines)
lines = [(l, True, idx) for idx, l in enumerate(lines)]

for l, c, lid in lines:
    if lid in safe_cnt:
        continue
    is_inc: bool | None = None
    prev = l[0]
    err_cnt = 0
    err_inc = False
    print(l)
    for idx, el in enumerate(l[1:]):
        print(idx)
        jump = abs(el - prev)
        if jump > 3 or jump == 0:
            if c:
                lcp1 = deepcopy(l)
                lcp2 = deepcopy(l)

                del lcp1[idx]
                print(f"adding {lcp1}")
                lines.append((lcp1, False, lid))

                del lcp2[idx + 1]
                print(f"adding {lcp2}")
                lines.append((lcp2, False, lid))
            break
        inc_new = el > prev
        if is_inc is None:
            is_inc = inc_new
        elif is_inc != inc_new:
            if c:
                lcp1 = deepcopy(l)
                lcp2 = deepcopy(l)
                lcp3 = deepcopy(l)

                del lcp1[idx]
                print(f"adding {lcp1}")
                lines.append((lcp1, False, lid))

                del lcp2[idx + 1]
                print(f"adding {lcp2}")
                lines.append((lcp2, False, lid))

                del lcp3[idx - 1]
                print(f"adding {lcp3}")
                lines.append((lcp3, False, lid))
            break
        prev = el
    else:
        print(f"safe #{lid}")
        safe_cnt[lid] = 1

for idx, l in enumerate(lines_orig):
    print(f"{idx}: {l} {idx in safe_cnt}")

print(len(safe_cnt.keys()))
