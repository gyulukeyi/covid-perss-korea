# coding: utf-8
# last update: 2022-05-09

"""Korean Sentimental Analysis based on KOSAC dictionary

This script performs a sentimental analysis over a Korean text using the KOSAC sentiment dictionary.

The script considers up to trigram and calculate the sentiment score for the input string.

KOSAC dictionary is announced with: 
    Shin, Hyopil, Munhyong Kim, Yu-Mi Jo, Hayeon Jang, and Andrew Cattle. 2013. KOSAC(Korean Sentiment Analysis Corpus): 
    한국어 감정 및 의견 분석 코퍼스, Information and Compuation, pages 181-190.
and can be accessed at:
    http://word.snu.ac.kr/kosac/lexicon.php

Author: Gyu-min Lee
his.nigel at gmail dot com
"""

import argparse

import pandas as pd

from typing import Optional

from konlpy import tag

try:
    from icecream import ic
except ImportError:  # Graceful fallback if IceCream isn't installed.
    ic = lambda *a: None if not a else (a[0] if len(a) == 1 else a)  # noqa

ic.disable() # ic is disabled by default UNLESS the main function calls for the debugging mode

def determine_tagger(name:str):
    
    """Determine the KoNLPy tagger based on the tagger name
    
    Parameters
    ----------
    name : str
        Name of the tagger
    
    Returns
    ---------
    tag.Tagger
        Tagger object
    """
    name = name.lower()

    if name == "hannanum":
        tagger = tag.Hannanum
    elif name == "kkma":
        tagger = tag.Kkma
    elif name == "komoran":
        tagger = tag.Komoran
    elif name == "mecab":
        tagger = tag.Mecab
    elif name == "okt" or name == "twitter":
        tagger = tag.Okt
    else:
        print("Refer to https://konlpy.org/en/latest/ for available taggers.")
        raise NameError

    return tagger

def load_sentiment_dictionary(filename:str = "./polarity.csv") -> dict:
    
    """Load a sentiment dictionary
    
    Load a sentiment dictionary from "filename". The method is designed for and tested with KOSAC Korean sentiment 
    dictionary. KOSAC is provided with several differnet files, but the current method is specifically intended to be 
    used with "polarity.csv". 

    While "polarity.csv" contains many valuable information, the current method simply assign a word to one of the three
    categories: positive, neutral, and negative. The resulting dictionary contains list of positive, neutral, and 
    negative words. The intensity of the positivity and negativity is not regarded. 

    Parameters
    -------------
    filename : str
        The name of the dictionary file
    
    Returns
    ------------
    dict{str: list}
        Dictionary of lists, keyed as "pos" for positive, "neut" for neutral, and "neg" for negative
    """

    try:
        sentiment_dictionary = pd.read_csv(filename)
        if len(sentiment_dictionary) < 3:
            raise FileNotFoundError
    except FileNotFoundError:
        print("Pelase get the polarity.csv-like dictionary file from KOSAC page.")
        print("http://word.snu.ac.kr/kosac/lexicon.php")
        exit()
    
    try:            
        positive = sentiment_dictionary.loc[sentiment_dictionary["max.value"] == "POS"]['ngram'].tolist()
        neutral = sentiment_dictionary.loc[sentiment_dictionary["max.value"] == "NEUT"]['ngram'].tolist()
        negative = sentiment_dictionary.loc[sentiment_dictionary["max.value"] == "NEG"]['ngram'].tolist()
    except KeyError:
        print("Please check the sentiment dictionary file format. It should resemble polarity.csv.")
        exit()
        
    result = {"pos": positive,
        "neut": neutral,
        "neg": negative}
    
    return result

def tokenize(sentence: str = "", tagger = tag.Mecab) -> str:


    """Tokenize the sentence and represent linearly.
    
    Use the tagger to tag the sentence. 
    The resulting sentence is linear with PoS tag attached with '/' so that it can match the format used in 
    "polarity.csv"

    Note that Mecab-ko tokenizer requires additional installation process.

    "polarity.csv" is assumed to be tagged with Sejong PoS tags. Unfortunately, taggers provided by KoNLPy does not 
    support Sejong PoS tags. Mecab-ko uses "similar" tag set, but not exactly same.
    For the list of the tag sets, see:
        https://docs.google.com/spreadsheets/d/1OGAjUvalBuX-oZvZ_-9tEfYD2gQe7hTGsgUpiiBSXI8/edit#gid=0

    Parameters
    --------------
    sentence : str
        The sentence to tokenize
    tagger : konlpy.tag.Tagger
        The tagger to use from konlpy

    Returns
    -------------
    str
        The tokenized, linear sentence. For example, "동해물과 백두산이" would be "동해/NNP 물/NNG 과/JC..."
    """

    pos_tagger = tagger()

    sentence_pos_tagged = pos_tagger.pos(sentence)

    sentence_pos_tagged_linear = ""
    for token in sentence_pos_tagged:
        sentence_pos_tagged_linear += token[0]
        sentence_pos_tagged_linear += "/"
        sentence_pos_tagged_linear += token[1]
        sentence_pos_tagged_linear += " "
    
    return sentence_pos_tagged_linear

def evaluate(sent_dict, token: str = "") -> Optional[int]:
    
    """Evaluate the token on the sent_dict
    
    Parameters
    ------------
    sent_dict : dict
        sentiment dictionary as load_sentiment_dictionary outputs
    token : str
        token to analyze. A unigram, bigram, or trigram.
    
    Returns
    ------------
    Optional[int]
        sentiment score. Return value is None if no match was found.
    """

    ic(token)

    if token in sent_dict["pos"]:
        sentiment_score = 1
    elif token in sent_dict["neut"]:
        sentiment_score = 0
    elif token in sent_dict["neg"]:
        sentiment_score = -1
    else:
        sentiment_score = None

    return sentiment_score

def analyze_unigram(sent_dict, sentence:str = "", checked_tokens:list = []) -> tuple[int, list]:
    
    """Analyze the sentence on the basis of unigram

    Parameters
    ---------
    sent_dict : dict
        sentiment dictionary as load_sentiment_dictionary() outputs
    sentence : str
        sentence to analyze the sentiment
    checked_tokens : list
        tokens already checked. Items should be unigram with PoS tag
    
    Returns
    ---------
    int
        sentiment score
    list
        list of unigrams checked in this method
    """    

    sentiment_score = 0
    tokens_checked_here = list() 

    for token in sentence.split(' '):
        if token in checked_tokens:
            continue
        else:
            ic()
            token_score = ic(evaluate(sent_dict, token))
            if token_score != None:
                sentiment_score += token_score
                tokens_checked_here.append(token)


    return sentiment_score, tokens_checked_here

def analyze_bigram(sent_dict, sentence:str = "", checked_tokens:list = []) -> tuple[int, list]:
    
    """Analyze the sentence on the basis of bigram
    
    Parameters
    ---------
    sent_dict : dict
        sentiment dictionary as load_sentiment_dictionary() outputs
    sentence : str
        sentence to analyze the sentiment
    
    Returns
    ---------
    int
        sentiment score
    list
        list of unigrams checked in this method
    """
    
    sentiment_score = 0
    tokens_checked_here = list()

    tokens = sentence.split(' ')

    for idx in range(len(tokens)-1):

        if tokens[idx] in checked_tokens and tokens[idx+1] in checked_tokens:
            continue
        else:
            ic()
            bigram = tokens[idx] + ";" + tokens[idx+1]
            
            bigram_score = ic(evaluate(sent_dict, bigram))
            if bigram_score != None:
                sentiment_score += bigram_score
                tokens_checked_here.append(tokens[idx])
                tokens_checked_here.append(tokens[idx+1]) 
    
    return sentiment_score, tokens_checked_here

def analyze_trigram(sent_dict, sentence:str = "", checked_tokens:list = []) -> tuple[int, list]:

    """Analyze the sentence on the basis of trigram
    
    Parameters
    ---------
    sent_dict : dict
        sentiment dictionary as load_sentiment_dictionary() outputs
    sentence : str
        sentence to analyze the sentiment
    
    Returns
    ---------
    int
        sentiment score
    list
        list of unigrams checked in this method
    """

    sentiment_score = 0
    tokens_checked_here = list()

    tokens = sentence.split(' ')

    for idx in range(len(tokens)-2):
        
        if tokens[idx] in checked_tokens and tokens[idx+1] in checked_tokens and tokens[idx+2] in checked_tokens:
            continue
        else:
            ic()

            trigram = tokens[idx] + ";" + tokens[idx+1] + ";" + tokens[idx+2]
            
            trigram_score = ic(evaluate(sent_dict, trigram))
            if trigram_score != None:
                sentiment_score += trigram_score
                tokens_checked_here.append(tokens[idx])
                tokens_checked_here.append(tokens[idx+1])                
                tokens_checked_here.append(tokens[idx+2])                
    
    return sentiment_score, tokens_checked_here

def analyze(sentence:str= "", level:int=3, sent_dict_filename:str="./polarity.csv", 
                tagger:str="mecab", no_tagging:bool=False) -> int:

    """Analyze the sentence
    
    This is the function to actually analyze the sentence.
    
    Parameters
    -----------
    sentence : str
        sentence to analyze the sentiment
    sent_dict_filename : str
        path to the sentiment dictionary
    tagger : str
        name of the tagger to use
    
    Returns
    ---------
    int
        sentiment score of the sentence
    """

    score = 0

    tagger = determine_tagger(tagger)
    sent_dict = load_sentiment_dictionary(sent_dict_filename)
    
    if no_tagging:
        tokenized_sentence = sentence
    else:
        tokenized_sentence = tokenize(sentence, tagger)
    
    if level == 3:
        trigram_score, trigram_checked_list = ic(analyze_trigram(sent_dict, tokenized_sentence))
        bigram_score, bigram_checked_list = ic(analyze_bigram(sent_dict, tokenized_sentence, trigram_checked_list))
        bi_tri_checked_list = trigram_checked_list + bigram_checked_list
        unigram_score, _ = ic(analyze_unigram(sent_dict, tokenized_sentence, bi_tri_checked_list))
    elif level == 2: 
        trigram_score = 0
        trigram_checked_list = list()
        bigram_score, bigram_checked_list = ic(analyze_bigram(sent_dict, tokenized_sentence, trigram_checked_list))
        bi_tri_checked_list = trigram_checked_list + bigram_checked_list        
        unigram_score, _ = ic(analyze_unigram(sent_dict, tokenized_sentence, bi_tri_checked_list))
    elif level == 1:
        bigram_score, trigram_score = 0, 0
        bigram_checked_list, trigram_checked_list = list(), list()
        bi_tri_checked_list = trigram_checked_list + bigram_checked_list        
        unigram_score, _ = ic(analyze_unigram(sent_dict, tokenized_sentence, bi_tri_checked_list))
    else: 
        assert RuntimeError("Level must be between 1 to 3")

    score = trigram_score + bigram_score + unigram_score
    
    return score

def main(sentence:str = "",
        level:int = 3,
        tagger:str = "mecab", 
        no_tagging:bool = False,
        sent_dict_filename:str = "./polarity.csv",
        debugging:bool = False):

    if debugging == True:
        ic.enable()

    score = analyze(sentence, level, sent_dict_filename, tagger, no_tagging)

    print(f"""The sentiment score of the following sentence is {score}.
    {sentence}
    """)

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog="kosac_sent_analyzer", 
                                    usage="%(prog)s [options] sentence",
                                    description="Sentiment analysis for Korean using KOSAC")
    
    parser.add_argument('sentence',
                        metavar='sentence',
                        nargs='+',
                        type=str,
                        help="Sentence to analyze")
    parser.add_argument('-l',
                        '--level',
                        type=int,
                        dest='level',
                        action='store',
                        default=3,
                        help="The depth of †he n-gram. An integer between 1 and 3.")
    parser.add_argument('-t',
                        '--tagger',
                        type=str,
                        action='store',
                        dest='tagger',
                        default='mecab',
                        help="Tagger to use")
    parser.add_argument('-n', 
                        '--no_tagging',
                        action='store_true',
                        default='0',
                        dest='no_tagging')
    parser.add_argument('-f',
                        '--file_name',
                        type=str,
                        dest='file_name',
                        action='store',
                        default='./polarity.csv',
                        help="File name for sentiment dictionary")
    parser.add_argument('-d',
                        '--debugging',
                        action='store_true',
                        default='0',
                        dest='debugging')
    
    arguments = parser.parse_args()

    main(sentence=' '.join(arguments.sentence),
        level=arguments.level,
        tagger=arguments.tagger,
        no_tagging=arguments.no_tagging,
        sent_dict_filename=arguments.file_name,
        debugging=arguments.debugging)