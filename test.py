map = [[0 for _ in range(5)] for _ in range(5)]
map[2] = [1]*5
map[3] = [1]*5
score = 0

for pos, row in enumerate(map):
    check = 1
    for column_ele in row:
        check &= column_ele
    if check == 1:
        score += 1
        del map[pos]
        map.insert(0, [0]*5)
    
print(score)
print(map)