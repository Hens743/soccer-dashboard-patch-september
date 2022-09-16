from typing import Dict, List
import json

import pandas as pd
import numpy as np

from preprocessing.data_loader import SoccerPlayer


def df_strip_nans(df: pd.DataFrame):
    first_idx = df.first_valid_index()
    last_idx = df.last_valid_index()
    return df.loc[first_idx:last_idx]


def get_injury_categories(players: List[SoccerPlayer]):
    injuries = [json.loads(item.type) for sublist in [player.injuries for player in players]
                 for item in sublist if json.loads(item.type)]
    processed_injuries = []
    for dicts in injuries:
        for key, value in dicts.items():
            processed_injuries.append((key, value))
    gathered = pd.DataFrame(processed_injuries, columns=["location", "severity"])
    return gathered.groupby(["location", "severity"]).size().unstack(fill_value=0)


def get_readiness_quantile_ts(players: List[SoccerPlayer]):
    time_idx = list(players)[0].readiness.index
    nan_df = pd.DataFrame(np.array([player.readiness for player in players]).T, index=time_idx)
    readiness_df = df_strip_nans(nan_df)
    median = readiness_df.apply(lambda x: np.nanmedian(x), axis=1)
    lower_quantile = readiness_df.apply(lambda x: np.nanquantile(x, 0.25), axis=1)
    higher_quantile = readiness_df.apply(lambda x: np.nanquantile(x, 0.75), axis=1)
    return pd.DataFrame({"median": median, "lower_quantile": lower_quantile, "higher_quantile": higher_quantile},
                        index=readiness_df.index)



#TO DO:
# Implement readiness graph with range values, least ready most ready
# High exhaustion training days for team: last week and general -- daily load
# Team Mood: Weighted Average of Mood, Stress, Readiness
# Team Fatigue: Weighted Average of Sleep duration, Sleep quality, fatigue, ACWR