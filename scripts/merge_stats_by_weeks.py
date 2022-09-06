# coding: utf-8

"""merge_stats_by_weeks.py

Merge the raw statistics by weekly basis.

Author: Gyu-min Lee 
his.nigel at gmail dot com
"""

import pandas as pd

from pandas.tseries.frequencies import to_offset

from icecream import ic
ic.disable()

def main(do_debug):
    if do_debug:
        ic.enable()
    
    df = pd.read_excel("./data/statistics.xlsx")
    df = df.set_index('일자').resample('1W', label='left').sum()
    df.index = df.index.to_pydatetime()
    df.index = df.index + to_offset("1D")
    df = df.drop(["순서"], axis=1)
    ic(df)
    df.to_excel("./data/statistics_wkly.xlsx")

if __name__ == "__main__":
    do_debug = False

    main(do_debug)