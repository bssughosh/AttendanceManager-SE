f1 = open('userdet.txt', 'r')
a = []
c=0
for row in f1.readlines():
    a.append(row)
    c+=1

for i in range(c-1):
    l = len(a[i])
    a[i] = a[i][:l-1]

print(a)
