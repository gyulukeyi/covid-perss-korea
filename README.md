# covid-press-korea

*This repository include data and scripts used for the following paper to appear in 30(3) of The Sociolinguistic Journal of Korea.*

> Lee, Gyu-min & Song, Sanghoun. (To Appear). The Korean Coronavirus Corpus: A Large-Scale Analysis Using Computational Skills. *The Sociolinguistic Journal of Korea, 30* (3).


**Assess the impact of the Korean media presses on COVID-related indexes.**

We construct a corpus comprised of COVID-related Korean articles, following BYU Coronavirus Corpus. 

We cannot share the corpus itself. Here, instead, we have made the following public for your reference:

- the corpus statistics
  - press distibution 
  - frequency and sentiment scores for the five keywords for covid, mask, (social) distancing, vaccine, and getting confirmed for the disease.
= the scripts for our research
  - date-based merger for the corpus files and statistics
  - NLTK-based concordance generator 
  - Sentiment analyzer based on the [KOSAC sentiment dictionary](http://word.snu.ac.kr/kosac/lexicon.php) (acutal dictionary not included -- go to the project's website for yours)
  - HuggingFace and PyTorch-based RoBERTa fine-tuner and sentiment classifier 
  - R script for the calculation of the Transfer Entropy usign RTransferEntropy
