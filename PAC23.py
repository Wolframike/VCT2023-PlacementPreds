import numpy as np
import random
import time
import os
from functools import reduce
from _func import *

# チーム数
N = 10

# Best of
BO = 3

# ボーダー
border = np.zeros((N, N + 1))

# 出力時の幅
w = 13

# 繰上げ桁
r = w - 4

# 取得ラウンドのテーブル
# まだ戦ってない試合には-1,同じチームがクロスするところには0
XX = -1
DD = 0
result = np.array([
    [DD,  0,  1,  0,  0,  0,  1, XX,  0,  0],#DFM
    [ 2, DD,  2,  2,  2,  2, XX,  2,  0,  2],#DRX
    [ 2,  1, DD,  0,  0,  2,  2,  0,  2,  1],#GEN
    [ 2,  0,  2, DD,  1,  0,  1,  2, XX,  1],#GE
    [ 2,  0,  2,  2, DD, XX,  2,  2,  1,  2],#PRX
    [ 2,  1,  0,  2, XX, DD,  0,  2,  2,  1],#RRQ
    [ 2, XX,  0,  2,  0,  2, DD,  2,  2,  2],#T1
    [XX,  0,  2,  0,  1,  1,  0, DD,  1,  2],#TLN
    [ 2,  2,  0, XX,  2,  0,  0,  2, DD,  1],#TS
    [ 2,  0,  2,  2,  0,  2,  1,  0,  2, DD],#ZETA
#   DFM DRX GEN  GE PRX RRQ  T1 TLN  TS ZETA
])


# 略称
Abbr = [
    "DFM",
    "DRX",
    "GEN",
    "GE",
    "PRX",
    "RRQ",
    "T1",
    "TLN",
    "TS",
    "ZETA"
]

#クロステーブル確認用
while True:
    yorn = input("Check the cross table? (y/n): ")
    if yorn == "y" or yorn == "n": break
    
if yorn == "y":
    TableCheck(result, Abbr, N, BO)

# それぞれのチームがどの順位になったかをカウント
count = np.zeros((N, N+1))

# 未実施の試合をremaining_matchへ格納
remaining_match = []
for i in range(N-1):
    for j in range(i+1, N):
        if result[i][j] == -1:
            remaining_match.append((i, j))

s = time.time()

fullsearch = False

if len(remaining_match) <= 10:
    print(f"Performing full search on {len(remaining_match)} matches...\n")
    count = matchFill(result, remaining_match, BO, N)
    fullsearch = True
    
else:
    print("Performing Monte Carlo simulation...\n")

    l, DIV = settings()# 試行回数設定とプログレスバーのヘッダー表示
    
    for _ in range(l):
        if _%(l/DIV) == 0:
            print("█", end="")
        
        newtable = np.array(result)# クロステーブルをコピー

        # 残りの試合について、ランダムに試合結果を生成すして、対戦表を埋めていく
        for i, j in remaining_match: # チーム i vs. チーム j について
            p, q = randomscore(BO)
            newtable[i][j] = p
            newtable[j][i] = q

        standings = get_standings(newtable, N)

        standings = sorted(standings, key = lambda x: tuple(-x[i] for i in range(2, max([len(i) for i in standings]))))
        
        for i in range(N):
            team_num = standings[i][0] # (i+1)位のチーム番号
            count[team_num][i] += 1
        '''
        if standings[7][0] == 9:
            print()
            TableCheck(newtable, Abbr, N, BO)
            for i in standings:
                print(f"{Abbr[i[0]]}: {i[2]} - {9 - i[2]}")
        '''
        
e = time.time()
t = int(e - s)

# 試行回数で割って、パーセントに直す
if fullsearch:
    prob = count / (4 ** len(remaining_match)) * 100
else:
    prob = count / l * 100

place = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th"]
print("\n")

# 確率出力

for i in place:
    print(i, end = "")
    l = w - len(i)
    print(" " * (l + 1), end = "")
    if int(i[:-2]) == N:
        print("Team Name")
        break

m = 0 
for i in prob:
    n = 0
    for j in i:
        if n == N:
            print(Abbr[m])
            continue
        print(round(j, r), end = "")
        l = w - len(str(round(j, r)))
        print("%"+ " " * l, end = "")
        n+=1
    m+=1

print(f"\nTime taken: {t // 60}m{t % 60}s\n")

# ボーダー出力
'''
for i in place:
    print(i, end = "")
    l = w - len(i)
    print(" " * (l + 1), end = "")
    if int(i[:-2]) == N:
        print("W/L")
        break

m = 1     
for i in border:
    n = 0
    for j in i:
        pct = round(j * 100 / sum(i), r)
        if n == N:
            print(f"{N - m}W{m - 1}L")
            continue
        print(pct, end = "")
        l = w - len(str(pct))
        print("%" + " " * l, end = "")
        n+=1
    m+=1
'''
print("\n" + __file__[45:])
os.system('afplay /System/Library/Sounds/Blow.aiff')
