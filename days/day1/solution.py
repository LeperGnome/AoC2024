FNAME = "./inp.txt"

with open(FNAME, "r") as f:
    lines = [l.strip().split(sep="   ") for l in f.readlines()]

cols = list(zip(*lines))
l1 = sorted(list(cols[0]))
l2 = sorted(list(cols[1]))

s = 0
for i in range(len(l1)):
    ntimes = len([j for j in l2 if j == l1[i]])
    s += ntimes * int(l1[i])

print(s)
