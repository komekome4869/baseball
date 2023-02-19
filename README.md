# baseball

## 目的
日本ハムの勝率と各選手の成績を予測する．まずは，日ハムの勝率を予測し，Twitterとの連携で，その日の勝率をツイートする．
   
## 方法
DNNを使って勝率を予測．
* 入力
    * 相手チームの先発情報
    * 対戦チーム
    * スタメン

* 出力
    * 勝率

## データ
```
.
└── baseball
    ├── data
    │   ├── hitter                      #野手の年度ごとの成績    
    │   ├── pitcher                     #投手の年度ごとの成績
    │   ├── rotation                    #チームごとの試合日程と先発
    │   ├── schedule                    #試合日程
    │   └── stamen                      #ファイターズスタメン
    ├── gen_data
    │   ├── data_download.py
    │   └── rot_data_download.py
    ├── analysis.py
    ├── data.ipynb
    ├── date_data_download.py
    └── twitter.py

```


