from copy import deepcopy

FNAME = "./inp.txt"

Point = tuple[int, int]

with open(FNAME, "r") as f:
    data = f.read().strip()

# empty spots have negative idx
data = [
    [-idx / 2, int(d), False] if idx % 2 != 0 else [int(idx / 2), int(d), False]
    for idx, d in enumerate(data)
]
print(data)

arr = []

# Pt. 1
#
# from collections import deque
# data = deque(data)
#
# while data:
#     idx, d = data.popleft()
#
#     if idx < 0: # free space
#         left = d
#         while data and left:
#             if data[-1][1] == 0 or data[-1][0] < 0:
#                 data.pop()
#                 continue
#
#             arr.append(data[-1][0])
#             data[-1][1] -= 1
#             left -= 1
#     else:
#         arr \
#         += [idx]*int(d)
#
# print(arr)
# print(sum(idx * el for idx, el in enumerate(arr)))


spos = len(data) - 1
while spos >= 0:
    sidx, svol, moved = deepcopy(data[spos])
    # skipping extra space or already moved files
    if sidx < 0 or moved:
        spos -= 1
        continue

    for epos, e in enumerate(data):
        eidx, ecap, _ = e
        if eidx < 0 and abs(eidx) < sidx and ecap >= svol:
            data[spos][0] *= -1
            # my file fits perfectly into empty block
            if ecap == svol:
                data[epos] = [sidx, svol, True]
                spos -= 1
            # my file fits into empty block, but there's extra space
            else:
                dv = ecap - svol
                data[epos] = [eidx, dv, False]
                data.insert(epos, [sidx, svol, True])
                # NOTE:
                # not doing `spos -= 1`, because i've added a new
                # element to array before current
            break
    spos -= 1

for idx, n, _ in data:
    if idx >= 0:
        arr += [idx] * n
    else:
        arr += [None] * n

print("".join(str(idx) if idx else "." for idx in arr))
print(sum(i * idx if idx else 0 for i, idx in enumerate(arr)))
