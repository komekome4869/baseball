import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import argparse

def parse_config():
    parser = argparse.ArgumentParser()                             
    parser.add_argument("--year", type=int, default=21)
    parser.add_argument("--past", action="store_true", help="過去のデータを取得するか")          

    return parser.parse_args()


def pitcher_data(config):
    year = config.year
    #Pitcher
    #Webページにアクセス
    if config.past:  
        url = 'https://baseball-data.com/{:2}/stats/pitcher3-all/ip3-1.html'.format(config.year)  
    else:
        url = 'https://baseball-data.com/stats/pitcher3-all/ip3-1.html'
        year = 22
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    #HTMLから表の部分を全て取得する．(該当箇所:tableタグ)
    table = soup.find_all('table')[0]

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
    df.to_csv('../data/pitcher/PitcherData_{}.csv'.format(year), sep=',', header=True, index = False)



def hitter_data(config):
    year = config.year
    #hitter
    #Webページにアクセス
    if config.past:  
        url = 'https://baseball-data.com/{:2}/stats/hitter3-all/avg-1.html'.format(config.year)  
    else:
        url = 'https://baseball-data.com/stats/hitter3-all/avg-1.html'
        year = 22
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')

    #HTMLから表の部分を全て取得する．(該当箇所:tableタグ)
    table = soup.find_all('table')[0]

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
    df.to_csv('../data/hitter/HitterData_{}.csv'.format(year), sep=',', header=True, index = False)



if __name__ == "__main__":
    config = parse_config()
    pitcher_data(config)
    hitter_data(config)