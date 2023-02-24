import pandas as pd
import argparse

def parse_config():
    parser = argparse.ArgumentParser()                             
    parser.add_argument("--year", type=int, default=21)         

    return parser.parse_args()

def main(config):

    input_data_df = pd.DataFrame()

    for i in range(config.year, 23):
        # 日ハムスタメンデータをロード
        train_df = pd.read_csv(f'../data/stamen/StamenData_{i}.csv')
        train_df = train_df.drop(["日付","スコア","責任投手"], axis=1)

        # 球場の置換
        train_df["球場"] = pd.factorize(train_df["球場"])[0]

        # チームの置換
        train_df["対戦相手"] = pd.factorize(train_df["対戦相手"])[0]

        #開始時刻の変換
        train_df["開始"] = train_df["開始"].str[:2]

        # 勝敗の置換
        train_df["勝敗"] = pd.factorize(train_df["勝敗"])[0]

        for j in range(9):
            train_df[f"{j+1}番"] = train_df[f"{j+1}番"].str.replace(" ","")

        # ==== 野手・投手情報以外のデータを抽出 ====
        train_else_df = train_df[["勝敗","対戦相手","球場","開始"]]

        # ==== スタメンデータの選手名を指標に変換 =====
        # 全球団の野手の指標を整形
        hitter_df = pd.read_csv(f'../data/hitter/HitterData_{i}.csv')
        hitter_df["選手名"] = hitter_df["選手名"].str.replace("　","")
        hitter_df = hitter_df.drop(["順位", "チーム"],axis=1) 
        train_stamen_df = train_df[["{}番".format(x + 1) for x in range(9)]]
        # スタメン->指標情報に変換
        for j in range(9):
            train_stamen_df = pd.merge(train_stamen_df, hitter_df, left_on=f"{j+1}番", 
                                        right_on="選手名", how="left", 
                                        suffixes=(None, f"_{j+1}")).drop(["選手名",f"{j+1}番"], axis=1)

        # ==== 先発を指標に変換 ====
        train_pitch_df = train_df["先発投手"]
        pitcher_df = pd.read_csv(f'../data/Pitcher/PitcherData_{i}.csv')
        pitcher_df["選手名"] = pitcher_df["選手名"].str.split("　").str.get(0)
        pitcher_df = pitcher_df[pitcher_df["チーム"]=="日本ハム"]
        pitcher_df = pitcher_df.drop(["順位", "チーム"],axis=1)
        train_pitch_df = pd.merge(train_pitch_df, pitcher_df, left_on="先発投手", right_on="選手名", 
                            how="left", suffixes=(None, f"_{i+1}")).drop(["選手名","先発投手"], axis=1)

        # ==== 野手情報・投手情報・その他の情報を結合 ====
        train_data_df = pd.concat([train_else_df, train_stamen_df, train_pitch_df],axis=1)
        #欠損値削除
        train_data_df = train_data_df.dropna()
        # 対象となる文字列
        character = '∞'
        # 対象文字列を含む列名を取得
        # 対象文字列を含む列名を取得
        for column in train_data_df.columns:
            if any(train_data_df[column]==character):
                train_data_df = train_data_df[~train_data_df[column].str.contains(character)]

        # 空のデータフレームに追加
        input_data_df = pd.concat([input_data_df, train_data_df], axis=0)


    input_data_df.to_csv("../data/input_data/data.csv")




if __name__ == "__main__":
    config = parse_config()
    main(config)