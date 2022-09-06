# coding: utf-8

import os

import re
import kiwipiepy

from tqdm import tqdm
from nltk.text import Text

from icecream import ic
ic.disable()

def grab_file_paths(root:str, ext:str=".txt") -> list:
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


def main(keyword, do_debug):

    if do_debug:
        ic.enable()

    kiwi = kiwipiepy.Kiwi()

    files = grab_file_paths("./data/COVID19/tagged_weekly", ".tsv")

    ic(files)

    print("Generating concordances for "+keyword)

    lookup_word = keyword
    lookup_word_path = re.sub('/', '_', lookup_word)
    
    try:
        os.mkdir(f"./data/conc_result_{lookup_word_path}")
        os.mkdir(f"./data/conc_result_{lookup_word_path}_glued")
    except OSError:
        pass

    for file in tqdm(files):
        
        ic(file)
        file_name = os.path.basename(file)
        ic(file_name)

        with open(file) as f:
            tokens = f.read()

        tokens = re.sub('\t', ' ', tokens)
        tokens = tokens.split(' ')
        
        ic(tokens[0])

        text = Text(tokens)

        conc = text.concordance_list(lookup_word, width=200, lines=None)
    
        with open(f"./data/conc_result_{lookup_word_path}_glued/{file_name}", 'w') as f:
            if ic(len(conc)) == 0:
                f.write('')
            else:
                for c in conc:
                    line = c.line
                    line = re.sub(r"\/\w+", '', line)
                    line = line.split(' ')
                    line = kiwi.glue(line)
                    f.write(line)
                    f.write('\n')

        with open(f"./data/conc_result_{lookup_word_path}/{file_name}", 'w') as f:
            if ic(len(conc)) == 0:
                f.write('')
            else:
                for c in conc:
                    line = c.line
                    f.write(line)
                    f.write('\n')

    print(f"Wrote concordances for {lookup_word}.")    
 
if __name__ == "__main__":
    keywords = ["코로나/NNP", "마스크/NNG", "확진/NNG", "거리두기/NNG", "백신/NNG"]
    do_debug = False

    for keyword in keywords:
        main(keyword, do_debug)  
