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



def gen_rot(config, team):
    #Webページにアクセス
    year = config.year
    if config.past:
        url = 'https://baseball-freak.com/rotation/{:2}/{}.html'.format(config.year,team)
    else:
        url = 'https://baseball-freak.com/rotation/{}-0.html'.format(team)
        year = 22
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')


    #HTMLから表の部分を全て取得する．(該当箇所:tableタグ)
    table = soup.find_all('table')[0]

    for tag in table.find_all('td', class_=['pad']):
        tag.decompose()
   

    #上記作成tableから行データを取得する．（該当箇所：trタグ）
    rows = table.find_all('td')

    #データ格納先
    HeadData = ['date','op_pitcher','team']       #'選手名',"チーム名"などデータの名前
    PlayerData = []     #[[選手1に関するデータ],[選手2に関するデータ]]

    # 行データから値を取り出す．
    for i, row in enumerate(rows):
        #細かいデータの取得
        PlayerRow = []
        PlayerRow.append(row.find("span").get_text())
        for PlayerValue in row.find_all('p',limit=2):
            print(PlayerValue)
            PlayerRow.append(PlayerValue.get_text())
        PlayerData.append(PlayerRow)


    #DataFrameに変換　表形式データ
    df = pd.DataFrame(data=PlayerData, columns=HeadData)
    #df = pd.DataFrame(data=PlayerData)

    #csvファイルに出力
    df.to_csv('../data/rotation/{}_{}.csv'.format(team,year), sep=',', header=True, index = False)

if __name__ == "__main__":
    config = parse_config()
    for team in ["fighters", "lions", "eagles", "hawks", "marines",
     "buffaloes", "giants", "tigers", "carp", "swallows", "dragons", "baystars"]:
        gen_rot(config, team)