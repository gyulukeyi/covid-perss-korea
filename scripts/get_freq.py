"""get_freq.py

Get absolute and relative frequencies from the tagged corpus.

Author: Gyu-min Lee
his.nigel at gmail dot com
"""

import os

from tqdm import tqdm 

import pandas as pd

def freq_per_mille(token: str, corpus: str) -> float:
    """Calculate the token's freuqency per million
    
    Parameters:
        token(str): the token on which the frequency is calculated
        corpus(str): the entire corpus
    
    Returns:
        float: the frequency per million
    """

    corpus_size = len(corpus.split(' '))
    token_freq = corpus.split(' ').count(token)
    
    result = token_freq / corpus_size
    result *= 1000000
    
    return result

def freq_absolute(token: str, corpus: str) -> int:
    """Calculate the token's absolute frequency
    
    Parameters:
        token(str): the token on which the frequency is calculated
        corpus(str): the entire corpus

    Returns:
        int: the frequency    
    """

    token_freq = corpus.split(' ').count(token)

    return token_freq

def main():
    keywords = ["코로나/NNP", "백신/NNG", 
            "확진/NNG", "마스크/NNG", "거리두기/NNG"]
    path = "./data/COVID19/tagged_weekly/"
    file_paths = os.listdir(path)
    
    result_list_abs, result_list_rel = list(), list()

    for file_path in tqdm(file_paths):
        list_abs = [file_path]
        list_rel = [file_path] 
        with open(f"{path}{file_path}") as file:
            content = file.read()
        for word in keywords:
            count_abs = freq_absolute(word, content)
            count_rel = freq_per_mille(word, content)
            list_abs.append(count_abs)
            list_rel.append(count_rel)
        result_list_abs.append(list_abs)
        result_list_rel.append(list_rel)
    
    result_df_abs = pd.DataFrame(result_list_abs, columns=["path", 
        "covid", "vaccine", "confirmed", "mask",
        "distancing"])

    result_df_abs.to_excel("./data/COVID19/tagged_weekly/freq_abs.xlsx")
    
    result_df_rel = pd.DataFrame(result_list_rel, columns=["path", 
        "covid", "vaccine", "confirmed", "mask",
        "distancing"])

    result_df_rel.to_excel("./data/COVID19/tagged_weekly/freq_rel.xlsx")

    print("Done.")

    return

if __name__ == "__main__":
    main()
