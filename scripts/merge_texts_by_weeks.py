# coding: utf-8

"""merge_texts_by_weeks.py

Merge the text files based on the date, which is given with its filename.

Author: Gyu-min Lee
his.nigel at gmail dot com
"""

import os
import re

from datetime import datetime

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
    
    paths.sort()
    
    return paths

def get_datetime(name: str) -> datetime:
    """grab datetime from the file name

    Params:
        name(str): the filename
    
    Returns;
        datetime: the timestamp from the file
    """

    date = re.search(r"\d{4}\.\d{2}\.\d{2}", name).group(0)
    date = datetime.strptime(date, "%Y.%m.%d")
    
    return date

def main(do_debug):
    if do_debug:
        ic.enable()
    
    print("Combining the corpus file (cleaned)...")

    os.mkdir("./data/COVID19/cleaned_weekly")

    paths = get_file_paths("./data/COVID19/cleaned")
    
    ic(paths)
    
    for i in tqdm(range(0, len(paths), 7)): 
        ic(paths[i])
        combined_path = get_datetime(paths[i])
        combined_path = combined_path.strftime("%Y.%m.%d")
        combined_path += "_wkly.tsv"
        ic(combined_path)

        with open(f"./data/COVID19/cleaned_weekly/{combined_path}", 'w') as file_combined:
            for j in range(7):
                with open(paths[i+j]) as file:
                    file_combined.write(file.read())
                    file_combined.write("\n")
    
    print("Wrote combined files to cleaned_weekly")

    print("Combining the corpus file (tagged)...")
    
    os.mkdir("./data/COVID19/tagged_weekly")

    paths = get_file_paths("./data/COVID19/tagged")
    
    ic(paths)

    for i in tqdm(range(0, len(paths), 7)): 
        ic(paths[i])
        combined_path = get_datetime(paths[i])
        combined_path = combined_path.strftime("%Y.%m.%d")
        combined_path += "_wkly.tsv"
        ic(combined_path)
        with open(f"./data/COVID19/tagged_weekly/{combined_path}", 'w') as file_combined:
            for j in range(7):
                with open(paths[i+j]) as file:
                    file_combined.write(file.read())
                    file_combined.write("\n")
    
    print("Wrote combined files to tagged_weekly")

    return

if __name__ == "__main__":
    
    do_debug = False

    main(do_debug)
