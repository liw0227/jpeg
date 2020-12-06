a = [1, 2, 3, 5, 6, 8, 9]
x = []
for i in range(len(a)):
    n = i - 1
    if n >= 0:
        t = a[i] - a[n]
        print(t)
        if t == 1:
            x.append(a[n])
print(x)
