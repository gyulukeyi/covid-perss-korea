# covid-press-korea

*This repository include data and scripts used for the following paper to appear in 30(3) of The Sociolinguistic Journal of Korea.*

> Lee, Gyu-min & Song, Sanghoun. (To Appear). The Korean Coronavirus Corpus: A Large-Scale Analysis Using Computational Skills. *The Sociolinguistic Journal of Korea, 30* (3).

**Assess the impact of the Korean media presses on COVID-related indexes.**

We construct a corpus comprised of COVID-related Korean articles, following BYU Coronavirus Corpus. 

We cannot share the corpus itself. Here, instead, we have made the following public for your reference:

- health stats
- the corpus statistics
  - press distibution 
  - frequency and sentiment scores for the five keywords for covid, mask, (social) distancing, vaccine, and getting confirmed for the disease.
- the scripts for our research
  - date-based merger for the corpus files and statistics
  - NLTK-based concordance generator 
  - Sentiment analyzer based on the [KOSAC sentiment dictionary](http://word.snu.ac.kr/kosac/lexicon.php) (acutal dictionary not included -- go to the project's website for yours)
  - HuggingFace and PyTorch-based RoBERTa fine-tuner and sentiment classifier 
  - R script for the calculation of the Transfer Entropy usign RTransferEntropy

For the details, refer to our paper (it's in English!). 

You are more than welcomed, under our license, to reuse the code with some modifications to run the analyses on your own data. 

For comments on the scripts, please email to Lee. For other comments, please contact Song (corresponding author). Addresses are in the paper, which will be uploaded here once publicly published.

## How to Run

1. Prepare all the data
	1. corpus (format under data/COVID19)
	2. `polarity.csv` from KOSAC project for dictionary-based sentiment analysis
2. Install required Python packages: `pip install -r requirements.txt`
3. Fine-tune a RoBERTa model for sentiment analysis with `./scripts/klue-RoBERTa-base-SA.ipynb`
	- fine-tuned model will be saved into `./resources/model_save' and can be reused for other Korean sentiment anlaysis tasks
	- if you want to use other models, change `./scripts/bert_SA.py` by changing the MODEL_PATH variable in line 141
	- if using a model from HuggingFace hub directly, in `./scripts/bert_SA.py`, set all `the local_files_only` parameters in `from_pretrained` method as `False`
4. Run the scripts: `sh run.sh`
5. Calculate the transfer entropy with `./scripts/calculate_TE.r`
	- This script will only print significant relations based on the $p$-value
6. Orgnize the transfer entropy results as `./results/TE_wkly_220810.xlsx`
	- Here, each cell is allocated for the transfer entropy value from the column name's variable to the row name's variable
	- e.g.,  O6 (0.129) means that absolute frequency for the word for 'vaccine' affected 3rd shot of vaccination by the transfer entroyp of 0.129
	- We only put the significant results. Thus, blanks mean that the transfer entropy was insignificant ($p > 0.05$). $p$-values are not recorded but all the values in the table got at least $p < 0.05$. The R script will put the actual $p$-value if only it is significant.
	- x is filled for the out-of-scope combinations. For instance, G8 is x because abolute frequency's affecting relatiive frequency for the word of *kholona* meaning covid is not in our interest -- it is not a linguistic feature affecting a health index.
	- Results in B7:F26 is not reported in the paper. They are the health indexes' affect on the linguistic use of the press. Here you can see that the reality is that the society affected the language use of the press much more than the other way around. This result is as valid and valuable as our reported result, but not reported since they can make our arguments blurry.
7. For better representation, make diagrams with boxes and arrows like the figures in the paper. We used PowerPoint and that was more than enough while being much easier to read than the excel files in (6).
