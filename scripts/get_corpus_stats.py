# coding: utf-8

"""get_corpus_stats.py

Calculate the corpus statistics from the Korean Coronavirus Corpus.

Will calculate:
    - number of articles per press in cleaned
    - number of ecels in cleaned
    - number of tokens in tagged

Author: Gyu-min Lee 
his.nigel at gmail dot com
"""

import os

import pandas as pd

from collections import Counter

from tqdm import tqdm

from icecream import ic
ic.disable()

def get_file_paths(root:str, ext:str=".tsv") -> list:
    """grab file paths in a path with certain extension
    
    Params:
        root(str): the root path
        ext(str): the extesion

    Returns:
        list: list of paths
    """

    paths = list()

    for file in os.listdir(root):
        if file.endswith(ext):
            paths.append(os.path.join(root, file))

    return paths

def get_press(article: str) -> str:
    """grab the press name from the article

    Params: 
        article(str): the article where the press name is separated by a '\t'
    Returns:
        str: the name of the press
    """
    article = article.split('\t')
   
    if len(article) < 2: # if no metadata available
        press = "NA"
    else:
        press = article[0]
    
    return press

def get_article_len(article: str) -> int:
    """grab an article and returns the true length

    Params:
        article(str): the artlce where the press name is seprated by a '\t'
    Returns:
        int: the length excluding the press name
    """
    article = article.split('\t')
    if len(article) < 2: # if no metadata available
        article = ' '.join(article)
    else:
        article = article[1:]
        article = ' '.join(article) # for just in case there is a tab in the body
    article = article.split(' ')
    length = len(article)
   
    return length

def count_press(paths: list) -> dict:
    """count presses in the paths

    Params:
        paths(list): list of paths to the articles.
    Returns:
        dict: press name and corresponding count.
    """

    press_names = list()

    for path in tqdm(paths):
        with open(path) as file:
            content = file.read()
        articles = content.split('\n')
        for article in articles:
            press = get_press(article)
            if "아시아?姸?" in press:
                ic(path)
                ic(press)
            press_names.append(press)
   
    count = Counter(press_names)
    count = count.most_common()
    count = dict(count)
    
    return count

def count_tokens(paths: list) -> int:
    """count tokens(spacing result) in the paths

    Params:
        paths(list): list of paths to the articles.
    Returns:
        int: number of tokens.
    """
    count = 0

    for path in tqdm(paths):
        with open(path) as file:
            content = file.read()
        articles = content.split('\n')
        for article in articles:
            count += get_article_len(article)

    return count

def main(do_debug):
    
    if do_debug:
        ic.enable()
    
    print("Loading the paths...")
    cleaned_paths = get_file_paths("./data/COVID19/cleaned")
    tagged_paths = get_file_paths("./data/COVID19/tagged")
    print("Paths loaded!")

    print("Counting the press...")
    press_count = count_press(cleaned_paths) 
    print("Press counted!")

    print("Counting the ecels...")
    ecel_count = count_tokens(cleaned_paths)
    print("Ecels counted!")

    print("Counting the words...")
    word_count = count_tokens(tagged_paths)
    print("Words counted!")

    print("========RESULT========")
    print(f"num_ecel:\t{ecel_count}")
    print(f"num_words:\t{word_count}")

    print("\nAlso saving the press count...")
    press_count_df = pd.DataFrame(press_count.items())
    press_count_df.to_excel("./results/press_count_result.xlsx", index=False)
    print("Count saved as ./results/press_count_result.xlsx")

    print("Done!")

if __name__ ==  "__main__":
    do_debug = False
    main(do_debug)
