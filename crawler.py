# for i in range(1993, 2020):
#     print(f"curl https://sports-statistics.com/database/soccer-data/england-premier-league-{i}-to-{i+1}.csv -o raw/{i}-{i+1}")
# http://www.football-data.co.uk/englandm.php

import pandas

all_data = None

for i in range(1993, 2020):
    df = pandas.read_csv(f"raw/{i}-{i+1}")
    if "Referee" not in df.columns:
        df["Referee"] = ""
    df = df[["Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "Referee"]]
    df = df[~df["Date"].isna()]
    df.rename(
        columns={
            "Date": "date",
            "HomeTeam": "home",
            "AwayTeam": "away",
            "FTHG": "home_score",
            "FTAG": "away_score",
            "Referee": "referee",
        },
        inplace=True,
    )
    df["season"] = f"{i}-{i+1}"
    df["home_score"] = df["home_score"].astype(int)
    df["away_score"] = df["away_score"].astype(int)

    if all_data is None:
        all_data = df
    else:
        all_data = pandas.concat([all_data, df], sort=False)

all_data.to_csv("data/data.csv", index=False)
