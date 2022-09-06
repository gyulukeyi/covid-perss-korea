# coding: utf-8

"""dict_SA.py
Performs sentiment analysis with PoS tagged text aggregated by week.

The results are to be saved as: dict_SA_wkly.csv in the concordance path.

Author: Gyu-min Lee 
his.nigel at gmail dot com
"""

import os
import sys

import pandas as pd

from datetime import datetime

from tqdm import tqdm
from tqdm.contrib.concurrent import process_map

from kosac_sent_analyzer import analyze

def get_avg_score(path:str) -> tuple([datetime, float]):
    """get average sentiment score from the path
    
    Params:
        path(str): path to the file
        
    Returns:
        (str, float): a tuple of the timestamp and the average score
    """
    
    timestamp = os.path.basename(path)
    timestamp = timestamp.rstrip("_wkly.tsv")
    timestamp = datetime.strptime(timestamp, "%Y.%m.%d")

    with open(path) as file:
        content = file.read()
    
    texts = content.split('\n')

    scores = list()

    for text in tqdm(texts, desc=f"Iterating for {timestamp}: ", position=1, leave=False):
        score = analyze(text, level=2, no_tagging=True)
        scores.append(score)

    avg_score = sum(scores)/len(scores)
    
    return (timestamp,avg_score)

def get_score(token:str) -> None:
    """get score for the token.

    Params:
        token(str): token to analyze. Should be with PoS tag e.g., 코로나_NNP
    Returns:
        None. It saves the data as a CSV file without returning anything.
    """
    
    print(f"Performing Dict-SA for {token}...")

    paths = list()

    for file in os.listdir(f"./data/conc_result_{token}/"):
        if file.endswith(".tsv"):
            paths.append(os.path.join(f"../conc_result_{token}/", file))
    
    results = process_map(get_avg_score, paths, desc="Master iter: ", position=0)

    df = pd.DataFrame(results, columns=["date", "score"])
    df = df.set_index("date")
    df = df.sort_index()
    
    df.to_csv(f"./data/conc_result_{token}/dict_SA_wkly.csv")

    print(f"Result saved as ./data/conc_result_{token}/dict_SA_wkly.csv!")
    
    print()

def main():
    tokens_to_analyze = ["확진_NNG", "백신_NNG", "거리두기_NNG", "마스크_NNG", "코로나_NNP"]

    for token in tokens_to_analyze:
        get_score(token)

if __name__ == "__main__":
    main()
