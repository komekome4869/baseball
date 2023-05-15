# baseball

## 目的
日本ハムのスタメンや対戦チームの情報から日ハムのその日の勝率を予測する．
   
## 方法
DNNを使って勝率を予測．
* 入力
    * 先発
    * スタメン
    * 対戦チーム
    * 球場

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


