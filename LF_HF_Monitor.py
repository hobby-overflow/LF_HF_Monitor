import pandas as pd
import numpy as np
import datetime as dt
from scipy.signal import lombscargle, welch
from scipy.interpolate import splrep, splev
import pandas.tseries.offsets as offsets
from dateutil import parser
from pytz import timezone

# csv読み込み
df = pd.read_csv("./data/2019-06-23.csv")
df = df.drop(0)
# カラムの名前を変更
df = df.rename(columns={"Unnamed: 0": "date", "value": "hr"})
df["test"] = [(dt.datetime.strptime(df["date"][i + 1], "%Y-%m-%d %H:%M:%S")) for i in range(0, len(df))]
start_time = df.iloc[0, 0]
st = int(parser.parse(start_time).timestamp())
df["elapsed_time"] = [int(parser.parse(i).timestamp()) - st for i in df["date"]]
df["rri"] = [(60 * 1000 / int(i)) for i in df["hr"]]
df.set_index("date", inplace=True)

'''
for i in df.index:
    datas = df.loc[i - offsets.Minute():i]
'''

# print(df[(df["test"] > dt.datetime(2019,6,13,13)) & (df["test"] < dt.datetime(2019,6,13,14))])

def dateRange(h, st, en):
    year = 2019
    mouth = 6
    day = 13

    start = dt.datetime(year, mouth, day, h, st)
    end = dt.datetime(year, mouth, day, h, en)
    return df[(df["test"] > start) & (df["test"] < end)]

print("Test")

# 一分間隔でグループにする
data = []

# 範囲指定で取り出す
# print(df[(df["test"] > dt.datetime(2019,6,13,0,1)) & (df["test"] < dt.datetime(2019,6,13,0,2))])

time_data = df["test"][5727:]
cnt = 0
# print(df[(df["test"] > dt.datetime(2019,6,13,14) - offsets.Minute(1))])
print("Start")
for i in time_data:
    cnt = 0
    # 一分前
    prev_time = i - offsets.Minute(1)
    # 検索スタート位置
    now_time = i
    datas = df[(df["test"] < now_time) & (df["test"] > prev_time)]
    if len(datas) <= 1:
        print("Nothing")
        continue
    time = datas["elapsed_time"]
    t = np.array(time)

    if len(t) <= 1:
        print("LF_HF is Zero")
        LF_HF = 0
    else:
        
        # calc Start
        rri = datas["rri"]
        ibi = np.array(rri)

        phi = round((4.0 * np.pi), 0)
        f = np.linspace(0.001, phi, 120000)

        Pgram = lombscargle(t, ibi, f, normalize=True)

        vlf = 0.04
        lf = 0.15
        hf = 0.4
        Fs = 250

        lf_freq_band = (f >= vlf) & (f <= lf)
        hf_freq_band = (f >= lf) & (f <= hf)

        dy = 1.0 / Fs
        LF = np.trapz(y=abs(Pgram[lf_freq_band]), x=None, dx=dy)
        HF = np.trapz(y=abs(Pgram[hf_freq_band]), x=None, dx=dy)
        LF_HF = float(LF) / HF
        df.at[str(i), "lf_hf"] = LF_HF
        print(str(i) + " : " + str(LF_HF))

    print(str(i) + ": " + str(df.at[str(i), "lf_hf"]))

#print(df["lf_hf"])

# 時 分 秒