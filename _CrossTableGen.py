import random

l = []
n = int(input("Team Number: "))
inner = []
for i in range(n):
    for j in range(n):
        if i == j:
            inner.append("DD")
        else:
            inner.append("XX")

    l.append(inner)
    inner = []

[print(str(i).replace("\'", "") + ",#") for i in l]
