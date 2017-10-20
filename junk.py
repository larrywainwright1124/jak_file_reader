s = '1234'

s = s[::-1]
inc = 1
val = 0
for c in s:
    val += (ord(c) - 48) * inc
    inc *= 10

print val
print type(val)




