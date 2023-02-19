import urllib.request
from bs4 import BeautifulSoup
import pandas as pd
import argparse


def parse_config():
    parser = argparse.ArgumentParser()                             
    parser.add_argument("--year", type=int, default=21)
    parser.add_argument("--past", action="store_true", help="過去のデータを取得するか")          

    return parser.parse_args()


def match_result(config):
    year = config.year
    # ===========- スタメンを取得 ===================
    #Webページにアクセス
    if config.past:  
        stamen_url = 'https://baseball-data.com/{:2}lineup/f.html'.format(config.year)  
    else:
        stamen_url = 'https://baseball-data.com/lineup/f.html'
        year = 22

    stamen_html = urllib.request.urlopen(stamen_url)
    soup = BeautifulSoup(stamen_html, 'html.parser')
    #HTMLから表の部分を全て取得する．(該当箇所:tableタグ)
    table = soup.find_all('table')[0]
    #上記作成tableから行データを取得する．（該当箇所：trタグ）
    rows = table.find_all('tr')

    #データ格納先
    stamen_HeadData = []       #'選手名',"チーム名"などデータの名前
    stamen_PlayerData = []     #[[選手1に関するデータ],[選手2に関するデータ]]
    # 行データから値を取り出す．
    for i, row in enumerate(rows):
        #表の１行目
        if i==0:
            #ヘッダの値を取得'選手名''チーム名',
            for HeaderValue in row.find_all('th'):
                stamen_HeadData.append(HeaderValue.get_text())

        #2行目~　ここの選手データ
        elif (i>0) and (i < len(rows)):
            #細かいデータの取得
            PlayerRow = []
            for PlayerValue in row.find_all('td'):  
                PlayerRow.append(PlayerValue.get_text().strip())
            stamen_PlayerData.append(PlayerRow)


    # ===========- 試合結果を取得 ===================
    #Webページにアクセス    
    if config.past:  
        result_url = 'https://baseball-freak.com/game/{:2}/fighters.html'.format(config.year)  
    else:
        result_url = 'https://baseball-freak.com/game/fighters.html'
    result_html = urllib.request.urlopen(result_url)
    soup = BeautifulSoup(result_html, 'html.parser')
    #HTMLから表の部分を全て取得する．(該当箇所:tableタグ)
    table = soup.find_all('table')[0]
    #上記作成tableから行データを取得する．（該当箇所：trタグ）
    rows = table.find_all('tr')

    #データ格納先
    result_HeadData = []       #'選手名',"チーム名"などデータの名前
    result_PlayerData = []     #[[選手1に関するデータ],[選手2に関するデータ]]
    # 行データから値を取り出す．
    for i, row in enumerate(rows):
        #表の１行目
        if i==0:
            #ヘッダの値を取得'選手名''チーム名',
            for HeaderValue in row.find_all('th'):
                result_HeadData.append(HeaderValue.get_text())

        #2行目~　ここの選手データ
        elif (i>0) and (i < len(rows)):
            #細かいデータの取得
            PlayerRow = []
            for PlayerValue in row.find_all('td'):  
                PlayerRow.append(PlayerValue.get_text().strip())
            result_PlayerData.append(PlayerRow)

    #DataFrameに変換　表形式データ
    stamen_df = pd.DataFrame(data=stamen_PlayerData, columns=stamen_HeadData)
    print(stamen_df.head())    
    result_df = pd.DataFrame(data=result_PlayerData, columns=result_HeadData) 
    result_df = result_df.loc[:,~result_df.columns.duplicated()]
    print(result_df.head())    

    df = pd.merge(stamen_df, result_df, on="日付")

    #csvファイルに出力
    df.to_csv('../data/stamen/StamenData_{}.csv'.format(year), sep=',', header=True, index = False)



if __name__ == "__main__":
    config = parse_config()
    match_result(config)

