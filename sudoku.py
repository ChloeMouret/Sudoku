import numpy as np
import requests


def mapping(x):
    return (x // 3) * 3


def check_value_possibilities(val, lig, col, tab, poss):
    a, b = mapping(lig), mapping(col)
    found = (val in tab[lig]) or (val in tab[:, col]) or (val in tab[a:a+3, b:b+3])
    if found:
        poss[lig][col].remove(val)
        return (True, False)
    else:
        if alone_in_line_column_square_possibilities(val, lig, col, poss):
            tab[lig, col] = val
            poss[lig][col] = []
            return (True, True)
        else:
            return (False, False)


def alone_in_line_column_square_possibilities(val, lig, col, poss):
    temp_line = []
    temp_column = []
    temp_square = []
    for y in range(9):
        if y != col:
            temp_line += poss[lig][y]
    for x in range(9):
        if x != lig:
            temp_column += poss[x][col]
    a, b = mapping(lig), mapping(col)
    for x in range(a, a + 3):
        for y in range(b, b + 3):
            if x != lig or y != col:
                temp_square += poss[x][y]
    return (val not in temp_line) or (val not in temp_column) or (val not in temp_square)


def initiate(t):
    possibilities = []
    for i in range(9):
        possibilities.append([])
        for j in range(9):
            if t[i, j] == 0:
                temp = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                possibilities[i].append(temp)
            else:
                possibilities[i].append([t[i, j]])
    return possibilities


def impossible(tab_val, tab_poss):
    error = False
    i = 0
    j = 0
    while not error and i < 9:
        j = 0
        while not error and j < 9:
            error = len(tab_poss[i][j]) == 0 and tab_val[i, j] == 0
            j += 1
        i += 1
    return error


def deep_list_copy(l):
    res = []
    for i in range(9):
        res.append([])
        for j in range(9):
            res[i].append(l[i][j].copy())
    return res


def compute(tab_t, tab_p):
    change = True
    while change:
        change = False
        for i in range(9):
            for j in range(9):
                for k in tab_p[i][j].copy():
                    temp = check_value_possibilities(k, i, j, tab_t, tab_p)
                    change = change or temp[0]
                    if temp[1]:
                        break
                if len(tab_p[i][j]) == 1:
                    tab_t[i, j] = tab_p[i][j][0]
                    tab_p[i][j] = []


def launch(tab):
    logs = []
    t = tab.copy()
    p = initiate(t)
    compute(t, p)
    if 0 in t:
        storage = []
        (i, j) = best_to_guess(p)
        storage.append({
            't': t.copy(),
            'p': deep_list_copy(p),
            'i': i,
            'j': j,
            'poss': p[i][j].copy()
        })
        while len(storage) > 0:
            while len(storage[-1]["poss"]) > 0:
                ak = storage[-1]["poss"].pop(0)
                tk = storage[-1]["t"].copy()
                pk = deep_list_copy(storage[-1]["p"])
                x,y = storage[-1]["i"], storage[-1]["j"]
                pk[x][y] = []
                tk[x, y] = ak
                compute(tk, pk)
                if not 0 in tk:
                    logs.append("("+str(x)+","+str(y)+") -> "+str(ak)+" | End")
                    return (tk, logs)
                elif impossible(tk, pk):
                    logs.append("("+str(x)+","+str(y)+") -> "+str(ak)+" | Impossible -> Rollback")
                    pass
                else:
                    logs.append("("+str(x)+","+str(y)+") -> "+str(ak)+" | Uncertain -> Continue")
                    (i, j) = best_to_guess(pk)
                    storage.append({
                        't': tk.copy(),
                        'p': deep_list_copy(pk),
                        'i': i,
                        'j': j,
                        'poss': pk[i][j].copy()
                    })
            storage.pop(-1)
        logs.append("WARNING : Should not be here")
        return (tab, logs)
    else:
        return (t, logs)


def best_to_guess(poss):
    i, j = 0, 0
    dic = dict()
    while i < 9:
        j = 0
        while j < 9:
            l = len(poss[i][j])
            if l == 2:
                return (i,j)
            if l != 0:
                dic[l] = (i,j)
            j += 1
        i += 1
    try:
        return dic[min(dic)]
    except:
        return (0,0)


def get_sudoku(difficulty):
    logs = []
    r = requests.get('http://www.cs.utep.edu/cheon/ws/sudoku/new/?size=9&level='+str(difficulty))
    data = r.json()
    logs.append("JSON successfully recovered : {}".format(data["response"]))
    tab = np.zeros((9, 9), dtype=int)
    for square in data["squares"]:
        tab[square["x"], square["y"]] = square["value"]
    logs.append("Board successfully initiated")
    return (tab, logs)