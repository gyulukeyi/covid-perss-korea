# coding: utf-8

"""bert_SA.py
Performs sentiment analysis with glued text aggregated by week.

The results are to be saved as: bert_SA_wkly.csv in the concordance path.

Author: Gyu-min Lee
his.nigel at gamil dot com
"""

import os
import sys

import numpy as np
import pandas as pd

import torch

from datetime import datetime

from torch.utils.data import Dataset
from torch.utils.data import DataLoader

from transformers import AutoTokenizer
from transformers import AutoModelForSequenceClassification

from tqdm import tqdm

torch.cuda.empty_cache()
torch.manual_seed(70)

class BertDataset(Dataset):
    def __init__(self, encodings):
        super().__init__()
        self.encodings = encodings

    def __len__(self):
        return len(self.encodings.input_ids)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        return item

def get_timestamp(path:str) -> str:
    """get timestamp str from path str.

    Params:
        path(str): path the the file
    Returns:
        str: the timestring in %Y.%m.%d format
    """

    timestamp = os.path.basename(path)
    timestamp = timestamp.rstrip("_wkly.tsv")
    timestamp = datetime.strptime(timestamp, "%Y.%m.%d")
    timestamp = str(timestamp).rstrip(" 00:00:00")
    
    return timestamp

def get_avg_score(path:str, 
                    tokenizer:AutoTokenizer,
                    model: AutoModelForSequenceClassification,
                    device: str
                    ) -> tuple([str, float]):
    """get average sentiment score from the path

    Params:
        path(str): path to the file
        tokenizer(AutoTokenizer): tokenizer to be used
        mode(AutoModelForSequenceClassification): model to predict the sentiment
        device(str): 'cuda' or 'cpu'

    Returns:
        (str, float): a tupe of the timestamp and the average score
    """
    MAX_LENGTH = 128
    BATCH_SIZE = 128

    timestamp = get_timestamp(path)
    
    with open(path) as file:
        contents = file.read().split('\n')

    contents_encoding = tokenizer(contents,
        max_length=MAX_LENGTH,
        truncation=True,
        padding=True)
    contents_dataset = BertDataset(contents_encoding)
    content_loader = DataLoader(contents_dataset,
                                batch_size=BATCH_SIZE,
                                shuffle=False)

    preds = list()

    model.eval()
    
    for batch in tqdm(content_loader,
                    desc=f"Iterating for {timestamp}: ",
                    position=1,
                    leave=False):
        input_ids = batch['input_ids'].to(device)
        attention_mask = batch['attention_mask'].to(device)

        with torch.no_grad():
            outputs = model(input_ids,
                        attention_mask=attention_mask)
            logits = outputs['logits']

            logits = logits.detach().cpu().numpy()

            pred = np.argmax(logits, axis=1)
            
            for p in pred:
                if p == 1:
                    preds.append(1)
                else:
                    preds.append(-1)

    avg_score = sum(preds)/len(preds)
    
    return (timestamp, avg_score)


def main():
    tokens_to_analyze = ["확진_NNG",
                         "백신_NNG",
                         "거리두기_NNG",
                         "마스크_NNG",
                         "코로나_NNP",
                         ]

    print("Running bert_SA.py...")
    DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

    if DEVICE == 'cpu':
        print("No CUDA device detected.")
        print("Will run using CPU... performance may be slow.")

    print("Loading the model: klue-RoBERTa-base-SA...")
    MODEL_PATH = "./resources/model_save/klue-RoBERTa-base-SA"
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH,
        local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH, 
        local_files_only=True,
        num_labels=2,
        output_attentions=False,
        output_hidden_states=False
        )

    model = model.to(DEVICE)
    print("Model has been loaded successfully!")

    for token in tokens_to_analyze:
        print(f"Performing BERT-SA for {token}...")

        paths = list()

        for file in os.listdir(f"./data/conc_result_{token}_glued/"):
            if file.endswith(".tsv"):
                paths.append(os.path.join(f"./data/conc_result_{token}_glued/", file))


        results = list()

        for path in tqdm(paths, position=0, desc="Master iter: "):
            result = get_avg_score(path, tokenizer, model, DEVICE) 
            results.append(result)

        df = pd.DataFrame(results, columns=["date", "score"])
        df = df.set_index("date")
        df = df.sort_index()

        df.to_csv(f"./data/conc_result_{token}_glued//bert_SA_wkly.csv")

        print(f"Result saved as ./data/conc_result_{token}_glued//bert_SA_wkly.csv!")
        print()

    return
    
if __name__ == "__main__":
    main()
