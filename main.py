import date_data_download
import gen_data.stamen_data_download as stamen_data_download
import twitter
import datetime
import pandas as pd

def main():
    #while True:
    # 日付を取得
    dt_now = datetime.datetime.now()
    # スケジュールを保存するpathを決定
    date_ym = "{:4}{:0>2}".format(dt_now.year, dt_now.month)
    date_ymd = "{:4}{:0>2}{:0>2}".format(dt_now.year, dt_now.month, dt_now.day)
    date_data_path = './data/schedule/{:6}.csv'.format(date_ym)

    # スケジュールcsvファイル作成
    date_data_download.generate_date_data(date_data_path,date_ym)

    # csvファイル読み込み
    csv_date = pd.read_csv(date_data_path)

    # 今日のデータを取得
    today_list = csv_date[csv_date.date==dt_now.day]

    # 今日の試合がない場合
    if(today_list.empty):
        twitter.CreateTweet("{:0>2}{:0>2}の試合なし".format(dt_now.month, dt_now.day))
    # 今日試合がある場合
    else:
        print(today_list)
        # 対戦相手の名前を取り出す
        opponent = today_list.iloc[:,1].values[0]
        # 時間とスタジアム名を取り出す
        time_stadium = today_list.iloc[:,2].values[0]
        # 時間部分だけ取り出す
        time = time_stadium[:2]
        # スタジアム名を取り出す
        stadium = time_stadium[9:]
        print("{:0>2}:00に{:}で{:}と試合".format(time, stadium, opponent))
        # スタメンダウンロード
        # 日付を取得
        dt_now = datetime.datetime.now()
        if(dt_now.hour >= int(time)):
            stamen_df = stamen_data_download.generate_stamen_data(date_ymd).values
            message = "{:0>2}:00に{:}で{:}と試合".format(time, stadium, opponent)
            message = message + '\n' + TwoDimListToStr(stamen_df)
            print(message)
            twitter.CreateTweet(message)

def TwoDimListToStr(two_d_list):
    message = ""
    for i, row in enumerate(two_d_list):
        for j , obj in enumerate(row):
            if(j<3):
                message += str(obj)
                message += ' '
        message +='\n'
    
    return message

if __name__ == "__main__":
    main()

