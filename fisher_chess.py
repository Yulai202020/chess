from random import randint

# Q - ферзь
# K - King
# Kn - Knight
# B - Bishop
# R - Rook

count = 0; id_list = []; result = ""
list1 = [1, 2, 3, 4, 5, 6, 7, 8]
g = ["B", "B", "N", "N", "R", "R", "K", "Q"]

while True:
    count = 0; id_list = []; result = ""

    while count != 8:
        randnum = randint(1, 8)
        if randnum not in id_list:
            count += 1
            id_list.append(randnum)
        else:
            continue

    Bishops_coords = []
    Rook_coords = []
    King_coord = 0

    for i in range(8):
        if id_list[i] == 1 or id_list[i] == 2:
            Bishops_coords.append(i)

        elif id_list[i] == 5 or id_list[i] == 6:
            Rook_coords.append(i)

        elif id_list[i] == 7:
            King_coord = i

        result += g[id_list[i]-1]
    
    if Bishops_coords[0] % 2 == Bishops_coords[1] % 2 or not (  King_coord > Rook_coords[0] and King_coord < Rook_coords[1] ):
        continue
    else:
        break

print(f"{result.lower()}/pppppppp/8/8/8/8/PPPPPPPP/{result} w KQkq - 0 1")