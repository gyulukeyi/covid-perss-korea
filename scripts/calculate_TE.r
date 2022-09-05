# calculate_TE.r
# calculate the transfer entropy with RTransferEntorpy package
# for 2022 COVID-ANALYSIS

# install.packages("RTransferEntropy")
library(RTransferEntropy)
library(readxl)

set.seed(37)

data <- read_excel("key_stats_wkly_220805.xlsx", 
                   col_types = c("date", "numeric", "numeric", "numeric", "numeric",
                                 "numeric", "numeric", "numeric", 
                                 "numeric", "numeric", "numeric", 
                                 "numeric", "numeric", "numeric", 
                                 "numeric", "numeric", "numeric", 
                                 "numeric", "numeric", "numeric", 
                                 "numeric", "numeric", "numeric", 
                                 "numeric", "numeric", "numeric"))

calc_and_print <- function(a, b){
  te <- transfer_entropy(a, b)
  
  if(te[3]$coef[, 4][1] < 0.05){
    print(te[3]$coef[, 1][1])
  } 
  if(te[3]$coef[, 4][2] < 0.05){
    print(te[3]$coef[, 1][2])
  } 
}

# =============
# ABS-Freq~stats
# =============

set_quiet(TRUE)

print("TE: covid_abs -> confirmed")
calc_and_print(data$covid_abs, data$confirmed)
print("TE: covid_abs -> died")
calc_and_print(data$covid_abs, data$died)

print("TE: covid_abs -> vaccine_1st")
calc_and_print(data$covid_abs, data$vaccine_1st)

print("TE: covid_abs -> vaccine_2nd")
calc_and_print(data$covid_abs, data$vaccine_2nd)

print("TE: covid_abs -> vaccine_3rd")
calc_and_print(data$covid_abs, data$vaccine_3rd)


print("TE: confirmed_abs -> confirmed")
calc_and_print(data$confirmed_abs, data$confirmed)

print("TE: confirmed_abs -> died")
calc_and_print(data$confirmed_abs, data$died)

print("TE: confirmed_abs -> vaccine_1st")
calc_and_print(data$confirmed_abs, data$vaccine_1st)

print("TE: confirmed_abs -> vaccine_2nd")
calc_and_print(data$confirmed_abs, data$vaccine_2nd)

print("TE: confirmed_abs -> vaccine_3rd")
calc_and_print(data$confirmed_abs, data$vaccine_3rd)


print("TE: vaccine_abs -> confirmed")
calc_and_print(data$vaccine_abs, data$confirmed)

print("TE: vaccine_abs -> died")
calc_and_print(data$vaccine_abs, data$died)

print("TE: vaccine_abs -> vaccine_1st")
calc_and_print(data$vaccine_abs, data$vaccine_1st)

print("TE: vaccine_abs -> vaccine_2nd")
calc_and_print(data$vaccine_abs, data$vaccine_2nd)

print("TE: vaccine_abs -> vaccine_3rd")
calc_and_print(data$vaccine_abs, data$vaccine_3rd)


print("TE: mask_abs -> confirmed")
calc_and_print(data$mask_abs, data$confirmed)

print("TE: mask_abs -> died")
calc_and_print(data$mask_abs, data$died)

print("TE: mask_abs -> vaccine_1st")
calc_and_print(data$mask_abs, data$vaccine_1st)

print("TE: mask_abs -> vaccine_2nd")
calc_and_print(data$mask_abs, data$vaccine_2nd)

print("TE: mask_abs -> vaccine_3rd")
calc_and_print(data$mask_abs, data$vaccine_3rd)


print("TE: distancing_abs -> confirmed")
calc_and_print(data$distancing_abs, data$confirmed)

print("TE: distancing_abs -> died")
calc_and_print(data$distancing_abs, data$died)

print("TE: distancing_abs -> vaccine_1st")
calc_and_print(data$distancing_abs, data$vaccine_1st)

print("TE: distancing_abs -> vaccine_2nd")
calc_and_print(data$distancing_abs, data$vaccine_2nd)

print("TE: distancing_abs -> vaccine_3rd")
calc_and_print(data$distancing_abs, data$vaccine_3rd)


# =============
# REL-Freq~stats
# =============

print("TE: covid_rel -> confirmed")
calc_and_print(data$covid_rel, data$confirmed)

print("TE: covid_rel -> died")
calc_and_print(data$covid_rel, data$died)

print("TE: covid_rel -> vaccine_1st")
calc_and_print(data$covid_rel, data$vaccine_1st)

print("TE: covid_rel -> vaccine_2nd")
calc_and_print(data$covid_rel, data$vaccine_2nd)

print("TE: covid_rel -> vaccine_3rd")
calc_and_print(data$covid_rel, data$vaccine_3rd)


print("TE: confirmed_rel -> confirmed")
calc_and_print(data$confirmed_rel, data$confirmed)

print("TE: confirmed_rel -> died")
calc_and_print(data$confirmed_rel, data$died)

print("TE: confirmed_rel -> vaccine_1st")
calc_and_print(data$confirmed_rel, data$vaccine_1st)

print("TE: confirmed_rel -> vaccine_2nd")
calc_and_print(data$confirmed_rel, data$vaccine_2nd)

print("TE: confirmed_rel -> vaccine_3rd")
calc_and_print(data$confirmed_rel, data$vaccine_3rd)


print("TE: vaccine_rel -> confirmed")
calc_and_print(data$vaccine_rel, data$confirmed)

print("TE: vaccine_rel -> died")
calc_and_print(data$vaccine_rel, data$died)

print("TE: vaccine_rel -> vaccine_1st")
calc_and_print(data$vaccine_rel, data$vaccine_1st)

print("TE: vaccine_rel -> vaccine_2nd")
calc_and_print(data$vaccine_rel, data$vaccine_2nd)

print("TE: vaccine_rel -> vaccine_3rd")
calc_and_print(data$vaccine_rel, data$vaccine_3rd)


print("TE: mask_rel -> confirmed")
calc_and_print(data$mask_rel, data$confirmed)

print("TE: mask_rel -> died")
calc_and_print(data$mask_rel, data$died)

print("TE: mask_rel -> vaccine_1st")
calc_and_print(data$mask_rel, data$vaccine_1st)

print("TE: mask_rel -> vaccine_2nd")
calc_and_print(data$mask_rel, data$vaccine_2nd)

print("TE: mask_rel -> vaccine_3rd")
calc_and_print(data$mask_rel, data$vaccine_3rd)


print("TE: distancing_rel -> confirmed")
calc_and_print(data$distancing_rel, data$confirmed)

print("TE: distancing_rel -> died")
calc_and_print(data$distancing_rel, data$died)

print("TE: distancing_rel -> vaccine_1st")
calc_and_print(data$distancing_rel, data$vaccine_1st)

print("TE: distancing_rel -> vaccine_2nd")
calc_and_print(data$distancing_rel, data$vaccine_2nd)

print("TE: distancing_rel -> vaccine_3rd")
calc_and_print(data$distancing_rel, data$vaccine_3rd)


# =============
# SA-dict~~stats
# =============

print("TE: covid_sa_dict -> confirmed")
calc_and_print(data$covid_sa_dict, data$confirmed)

print("TE: covid_sa_dict -> died")
calc_and_print(data$covid_sa_dict, data$died)

print("TE: covid_sa_dict -> vaccine_1st")
calc_and_print(data$covid_sa_dict, data$vaccine_1st)

print("TE: covid_sa_dict -> vaccine_2nd")
calc_and_print(data$covid_sa_dict, data$vaccine_2nd)

print("TE: covid_sa_dict -> vaccine_3rd")
calc_and_print(data$covid_sa_dict, data$vaccine_3rd)


print("TE: confirmed_sa_dict -> confirmed")
calc_and_print(data$confirmed_sa_dict, data$confirmed)

print("TE: confirmed_sa_dict -> died")
calc_and_print(data$confirmed_sa_dict, data$died)

print("TE: confirmed_sa_dict -> vaccine_1st")
calc_and_print(data$confirmed_sa_dict, data$vaccine_1st)

print("TE: confirmed_sa_dict -> vaccine_2nd")
calc_and_print(data$confirmed_sa_dict, data$vaccine_2nd)

print("TE: confirmed_sa_dict -> vaccine_3rd")
calc_and_print(data$confirmed_sa_dict, data$vaccine_3rd)


print("TE: vaccine_sa_dict -> confirmed")
calc_and_print(data$vaccine_sa_dict, data$confirmed)

print("TE: vaccine_sa_dict -> died")
calc_and_print(data$vaccine_sa_dict, data$died)

print("TE: vaccine_sa_dict -> vaccine_1st")
calc_and_print(data$vaccine_sa_dict, data$vaccine_1st)

print("TE: vaccine_sa_dict -> vaccine_2nd")
calc_and_print(data$vaccine_sa_dict, data$vaccine_2nd)

print("TE: vaccine_sa_dict -> vaccine_3rd")
calc_and_print(data$vaccine_sa_dict, data$vaccine_3rd)


print("TE: mask_sa_dict -> confirmed")
calc_and_print(data$mask_sa_dict, data$confirmed)

print("TE: mask_sa_dict -> died")
calc_and_print(data$mask_sa_dict, data$died)

print("TE: mask_sa_dict -> vaccine_1st")
calc_and_print(data$mask_sa_dict, data$vaccine_1st)

print("TE: mask_sa_dict -> vaccine_2nd")
calc_and_print(data$mask_sa_dict, data$vaccine_2nd)

print("TE: mask_sa_dict -> vaccine_3rd")
calc_and_print(data$mask_sa_dict, data$vaccine_3rd)


print("TE: distancing_sa_dict -> confirmed")
calc_and_print(data$distancing_sa_dict, data$confirmed)

print("TE: distancing_sa_dict -> died")
calc_and_print(data$distancing_sa_dict, data$died)

print("TE: distancing_sa_dict -> vaccine_1st")
calc_and_print(data$distancing_sa_dict, data$vaccine_1st)

print("TE: distancing_sa_dict -> vaccine_2nd")
calc_and_print(data$distancing_sa_dict, data$vaccine_2nd)

print("TE: distancing_sa_dict -> vaccine_3rd")
calc_and_print(data$distancing_sa_dict, data$vaccine_3rd)


# =============
# SA-BERT-Freq~stats
# =============

print("TE: covid_sa_bert -> confirmed")
calc_and_print(data$covid_sa_bert, data$confirmed)

print("TE: covid_sa_bert -> died")
calc_and_print(data$covid_sa_bert, data$died)

print("TE: covid_sa_bert -> vaccine_1st")
calc_and_print(data$covid_sa_bert, data$vaccine_1st)

print("TE: covid_sa_bert -> vaccine_2nd")
calc_and_print(data$covid_sa_bert, data$vaccine_2nd)

print("TE: covid_sa_bert -> vaccine_3rd")
calc_and_print(data$covid_sa_bert, data$vaccine_3rd)


print("TE: confirmed_sa_bert -> confirmed")
calc_and_print(data$confirmed_sa_bert, data$confirmed)

print("TE: confirmed_sa_bert -> died")
calc_and_print(data$confirmed_sa_bert, data$died)

print("TE: confirmed_sa_bert -> vaccine_1st")
calc_and_print(data$confirmed_sa_bert, data$vaccine_1st)

print("TE: confirmed_sa_bert -> vaccine_2nd")
calc_and_print(data$confirmed_sa_bert, data$vaccine_2nd)

print("TE: confirmed_sa_bert -> vaccine_3rd")
calc_and_print(data$confirmed_sa_bert, data$vaccine_3rd)


print("TE: vaccine_sa_bert -> confirmed")
calc_and_print(data$vaccine_sa_bert, data$confirmed)

print("TE: vaccine_sa_bert -> died")
calc_and_print(data$vaccine_sa_bert, data$died)

print("TE: vaccine_sa_bert -> vaccine_1st")
calc_and_print(data$vaccine_sa_bert, data$vaccine_1st)

print("TE: vaccine_sa_bert -> vaccine_2nd")
calc_and_print(data$vaccine_sa_bert, data$vaccine_2nd)

print("TE: vaccine_sa_bert -> vaccine_3rd")
calc_and_print(data$vaccine_sa_bert, data$vaccine_3rd)


print("TE: mask_sa_bert -> confirmed")
calc_and_print(data$mask_sa_bert, data$confirmed)

print("TE: mask_sa_bert -> died")
calc_and_print(data$mask_sa_bert, data$died)

print("TE: mask_sa_bert -> vaccine_1st")
calc_and_print(data$mask_sa_bert, data$vaccine_1st)

print("TE: mask_sa_bert -> vaccine_2nd")
calc_and_print(data$mask_sa_bert, data$vaccine_2nd)

print("TE: mask_sa_bert -> vaccine_3rd")
calc_and_print(data$mask_sa_bert, data$vaccine_3rd)


print("TE: distancing_sa_bert -> confirmed")
calc_and_print(data$distancing_sa_bert, data$confirmed)

print("TE: distancing_sa_bert -> died")
calc_and_print(data$distancing_sa_bert, data$died)

print("TE: distancing_sa_bert -> vaccine_1st")
calc_and_print(data$distancing_sa_bert, data$vaccine_1st)

print("TE: distancing_sa_bert -> vaccine_2nd")
calc_and_print(data$distancing_sa_bert, data$vaccine_2nd)

print("TE: distancing_sa_bert -> vaccine_3rd")
calc_and_print(data$distancing_sa_bert, data$vaccine_3rd)
