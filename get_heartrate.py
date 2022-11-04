import fitbit
from ast import literal_eval
import pandas as pd
from secret import CLIENT_ID, CLIENT_SECRET

tokens = open("token.json").read()
token_dict = literal_eval(tokens)
access_token = token_dict["access_token"]
refresh_token = token_dict["refresh_token"]


def updateToken(token):
    print(token)
    f = open("token.txt", "w")
    f.write(str(token))
    f.close()
    return


def get_heartrate_data():
    client = fitbit.Fitbit(
            CLIENT_ID,
            CLIENT_SECRET,
            access_token=access_token,
            refresh_token=refresh_token,
            refresh_cb=updateToken)

    DATE = "2022-10-31"
    data_sec = client.intraday_time_series(
            "activities/heart",
            DATE,
            detail_level="1min")

    heart_sec = data_sec["activities-heart-intraday"]["dataset"]
    heart_df = pd.DataFrame.from_dict(heart_sec)
    heart_df.to_csv(f"data/{DATE}.csv", header=False, index=False)
    print(heart_df)


get_heartrate_data()
