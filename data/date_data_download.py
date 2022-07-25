import urllib.request
from bs4 import BeautifulSoup
import pandas as pd

def generate_date_data(savepath, date):
    #Webページにアクセス
    url = 'https://www.fighters.co.jp/event/calendar/{:6}/index.html'.format(date)
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    #HTMLから表の部分を全て取得する．(該当箇所:tableタグ)
    table = soup.find_all('table')[0]

    #上記作成tableから行データを取得する．（該当箇所：trタグ）
    rows = table.find_all('td')

    #データ格納先
    HeadData = ['date','team','time_stadium']       #'選手名',"チーム名"などデータの名前
    PlayerData = []     #[[選手1に関するデータ],[選手2に関するデータ]]

    # 行データから値を取り出す．
    for i, row in enumerate(rows):
    
        #2行目~　ここの選手データ
        if (i>0) and (i+1 < len(rows)):
            #細かいデータの取得
            PlayerRow = []
            for PlayerValue in row.find_all('p',class_=['pl_date01 pl_bgHome','pl_teamName','pl_open']):
                print(PlayerValue)
                PlayerRow.append(PlayerValue .get_text().strip())
            PlayerData.append(PlayerRow)


    #DataFrameに変換　表形式データ
    df = pd.DataFrame(data=PlayerData, columns=HeadData)
    #df = pd.DataFrame(data=PlayerData)

    #csvファイルに出力
    df.to_csv(savepath, sep=',', header=True, index = False)