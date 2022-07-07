import pandas as pd

df = pd.read_csv('./data/playerData.csv',sep=',')

df11 = df[df['チーム'] != '日本ハム']
df_h = df[df['チーム'] == '日本ハム']

# 本塁打との相関係数をDataFrameとして変数に保存
df_homerun = pd.DataFrame(df11.corr()['本塁打'])
#相関係数[0.8]以上の項目名を抽出
X_columns = df_homerun[df_homerun['本塁打']>=0.8].index.tolist()
X_columns.remove('本塁打')
X = df11[X_columns]
y = df11['本塁打']

print(X)