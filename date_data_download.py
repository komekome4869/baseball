import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import argparse

def parse_config():
    parser = argparse.ArgumentParser()                             
    parser.add_argument("--year", type=int, default=21)
    # ロッテ:marines 楽天:eagles ソフト：hawks 西武：lions オリックス:buffaloes ヤクルト:swallows 横浜baystars 阪神:tigers 巨人:giants 広島:carp 中日:dragons
    parser.add_argument("--team", type=str, default="fighters") 
    parser.add_argument("--past", action="store_true", help="過去のデータを取得するか")          

    return parser.parse_args()



def gen_rot(config):
    #Webページにアクセス
    if config.past:
        url = 'https://baseball-freak.com/rotation/{:2}/{}.html'.format(config.year,config.team)
    else:
        url = 'https://baseball-freak.com/rotation/{}-0.html'.format(config.team)
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    #HTMLから表の部分を全て取得する．(該当箇所:tableタグ)
    table = soup.find_all('table')[0]

    #上記作成tableから行データを取得する．（該当箇所：trタグ）
    rows = table.find_all('td')

    #データ格納先
    HeadData = ['date','op_pitcher']       #'選手名',"チーム名"などデータの名前
    PlayerData = []     #[[選手1に関するデータ],[選手2に関するデータ]]

    # 行データから値を取り出す．
    for i, row in enumerate(rows):
    
        #2行目~　ここの選手データ
        if (i>0) and (i+1 < len(rows)):
            #細かいデータの取得
            PlayerRow = []
            for PlayerValue in row.find_all("p",class_=['c-date','c-starter c-st-4']):
                print(PlayerValue)
                PlayerRow.append(PlayerValue .get_text().strip())
            PlayerData.append(PlayerRow)


    #DataFrameに変換　表形式データ
    df = pd.DataFrame(data=PlayerData, columns=HeadData)
    #df = pd.DataFrame(data=PlayerData)

    #csvファイルに出力
    df.to_csv('../data/rotation/{}_{}.csv'.format(config.team,config.year), sep=',', header=True, index = False)

if __name__ == "__main__":
    config = parse_config()
    gen_rot(config)