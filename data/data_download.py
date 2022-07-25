import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

#Webページにアクセス
url = 'https://baseball-data.com/21/stats/hitter2-all/tpa-1.html'
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, 'html.parser')

#HTMLから表の部分を全て取得する．(該当箇所:tableタグ)
table = soup.find_all('table')[1]

#上記作成tableから行データを取得する．（該当箇所：trタグ）
rows = table.find_all('tr')

#データ格納先
HeadData = []       #'選手名',"チーム名"などデータの名前
PlayerData = []     #[[選手1に関するデータ],[選手2に関するデータ]]

# 行データから値を取り出す．
for i, row in enumerate(rows):
    #表の１行目
    if i==0:
        #ヘッダの値を取得'選手名''チーム名',
        for HeaderValue in row.find_all('th'):
            HeadData.append(HeaderValue.get_text())
    
    #2行目~　ここの選手データ
    elif (i>0) and (i+1 < len(rows)):
        #細かいデータの取得
        PlayerRow = []
        for PlayerValue in row.find_all('td'):
            PlayerRow.append(PlayerValue.get_text())
        PlayerData.append(PlayerRow)


#DataFrameに変換　表形式データ
df = pd.DataFrame(data=PlayerData, columns=HeadData)

#csvファイルに出力
df.to_csv('./PlayerData.csv', sep=',', header=True, index = False)