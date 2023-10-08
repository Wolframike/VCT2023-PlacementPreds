import numpy as np
import random
from functools import reduce


def TableCheck(result, Abbr, N, BO):
    for i in range(N):
        print("| ", end = "")
        for j in range(N):
            if result[i][j] == -1 and result[j][i] == -1:
                print("    | ", end = "")
            elif result[i][j] == -1 or result[j][i] == -1:
                print()
                raise ValueError(f"Only one side of the crosstable is filled: {Abbr[i]} vs {Abbr[j]}")
            elif result[i][j] > ((BO + 1) / 2) or result[j][i] > ((BO + 1) / 2):
                print()
                raise ValueError(f"Map count exceeding given maximum: {Abbr[i]} vs {Abbr[j]}")
            elif i != j:
                print(f"{result[i][j]}-{result[j][i]} | ", end = "")
            else:
                print("--- | ", end = "")
        print(Abbr[i])
    print("  ", end = "")
    [print(i + " " * (6 - len(i)), end = "") for i in Abbr]
    print("\n")
    

def get_standings(result, N):
    wins = [0] * N    # 勝利数
    #勝数の計算
    for i in range(N-1):
        for j in range(i+1, N):
            # i:チーム A vs. j:チーム B
            if result[i][j] == -1: # まだ対戦していないとき
                continue
            u = result[i][j] # チームA取得ラウンド数
            v = result[j][i] # チームB取得ラウンド数

            # 勝敗によって勝ち点の分配
            if u > v:
                wins[i] += 1
            else:
                wins[j] += 1

    #同勝ち点の勝ち数(H2H tiebreaker)
    H2Hwins = [0] * N # 直接対決の勝利数
    for i in range(N-1):
        for j in range(i+1, N):
            # i:チーム A vs. j:チーム Bで勝ち点が同じチーム同士の対戦について勝利数をカウントする
            if wins[i] != wins[j] or result[i][j] == -1:
                continue
            u = result[i][j] # チームA取得マップ数
            v = result[j][i] # チームB取得マップ数
            if u > v:
                H2Hwins[i] += 1
            else:
                H2Hwins[j] += 1

    # とりあえずの順位
    standings = []
    for i in range(N):
        # 得マップ数は横方向に和をとる
        # 失マップ数は縦方向に和をとる
        # maxを入れて-1を0にしておく
        map_win = sum([max(_, 0) for _ in result[i]])
        map_lost = sum([max(_, 0) for _ in result[:, i]])

        # 得失マップ差
        map_diff = map_win - map_lost

        # 0:チーム番号 1:diff 2:勝利数
        standings.append((i, map_diff, wins[i]))
        
    tieB = [0] * N
    tieA = [0] * N
    
    while True:
        # まだ引き分けているチームに対してH2Hを取る
        
        diff = [0] * N
        finalH2H = [0] * N
        tieB = [0] * N
        rand = [0] * N
        c = set()
        for i in range(N-1):
            for j in range(i+1, N):
                a = standings[i]
                b = standings[j]
                if reduce(lambda x, y: x and y, [a[n] == b[n] for n in range(2, len(a))]):
                    t1 = a[0]
                    t2 = b[0]

                    tieB[t1] += 1
                    tieB[t2] += 1
                    
                    u = result[t1][t2] # チームA取得マップ数
                    v = result[t2][t1] # チームB取得マップ数
                    if u > v:
                        finalH2H[t1] += 1
                    else:
                        finalH2H[t2] += 1

        for i in range(N):
            if tieB[i] == tieA[i] and len(standings[i]) > 4:
                rand[i] = random.randrange(-1, 2, 2)
                        
        # standingsにH2Hを反映
        for i in range(N):
            temp = list(standings[i])
            temp.append(finalH2H[i])
            temp.append(rand[i])
            standings[i] = tuple(temp)

        tieA = [0] * N

        # まだ引き分けているチームにMap diffをくっつける
        for i in range(N - 1):
            for j in range(i + 1, N):
                a = standings[i]
                b = standings[j]
                if reduce(lambda x, y: x and y, [a[n] == b[n] for n in range(2, len(a))]):
                    tieA[a[0]] += 1
                    tieA[b[0]] += 1
                    
                    diff[i] = a[1]
                    diff[j] = b[1]
                    
        # standingsにMap diffを反映
        for i in range(N):
            if tieB[i] != tieA[i]:
                diff[i] = 0
                
            temp = list(standings[i])
            temp.append(diff[i])
            standings[i] = tuple(temp)

        # 全てのタイブレイカーが固有なら終わり
        for i in standings:
            c.add(i[2:])
        
        if len(c) == len(standings):
            break

    return standings
    
def randomscore(BO):
    u = 0 # チームAの取得ラウンド
    v = 0 # チームBの取得ラウンド
    while True:
        if u == (BO + 1)/2 or v == (BO + 1)/2:
            break # 試合結果が決まったらループを出る
        
        b = random.randint(1, 2) # 1か2をランダムで決定
        
        if b == 1:
            u+=1 # チームAのマップ勝利
        if b == 2:
            v+=1 # チームBのマップ勝利
            
    return u, v

def settings():
    # 試行回数設定
    
    l = 5000 # 5000
    DIV = 40 # 40
    while True:
        horl = input("Heavy simulation or light? (h/l): ")
        if horl == "h" or horl == "l": break

    if horl == "h":
        l = 1000000
        DIV = 100

    # シミュレーション
    GAP = (DIV - 24) // 4
    print("0 %/" + "-" * GAP + "/25%/" + "-" * GAP + "/50%/" + "-" * GAP + "/75%/" + "-" * GAP + "/100%")

    return (l, DIV)
    
def matchFill(result, remaining_match, BO, N):
    if remaining_match == []:
        standings = get_standings(result, N)
        standings = sorted(standings, key = lambda x: tuple(-x[i] for i in range(2, max([len(i) for i in standings]))))
        count = np.zeros((N, N + 1))

        '''
        Abbr = ["DFM","DRX","GEN","GE","PRX","RRQ","T1","TLN","TS","ZETA"]
        
        if standings[PLACEMENT][0] == Abbr.index("TEAMNAME"):
            TableCheck(result, Abbr, N, BO)
            print(standings)
        '''
        
        for i in range(N):
            count[standings[i][0]][i] += 1

        return count

    twozero = result.copy()
    twoone = result.copy()
    onetwo = result.copy()
    zerotwo = result.copy()

    m = remaining_match[0]
        
    twozero[m[0]][m[1]] = 2
    twozero[m[1]][m[0]] = 0

    twoone[m[0]][m[1]] = 2
    twoone[m[1]][m[0]] = 1

    onetwo[m[0]][m[1]] = 1
    onetwo[m[1]][m[0]] = 2

    zerotwo[m[0]][m[1]] = 0
    zerotwo[m[1]][m[0]] = 2

    tz = matchFill(twozero, remaining_match[1:], BO, N)
    to = matchFill(twoone, remaining_match[1:], BO, N)
    ot = matchFill(onetwo, remaining_match[1:], BO, N)
    zt = matchFill(zerotwo, remaining_match[1:], BO, N)

    summed = np.zeros((N, N + 1))

    for i in range(N):
        for j in range(N + 1):
            summed[i][j] += (tz[i][j] + to[i][j] + ot[i][j] + zt[i][j])
    
    return summed
