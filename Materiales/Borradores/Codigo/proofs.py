from functools import reduce

tup = (2,1,0,2,2,0,0,2)
print(reduce(lambda x, y: x+y, tup))