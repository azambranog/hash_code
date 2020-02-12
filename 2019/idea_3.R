library(data.table)
source('format_as_tables.R')

datax <- format_as_table('b_lovely_landscapes.txt')

alltagsx <- expand_tags(datax)

data <- copy(datax)
alltags <- copy(alltagsx)

alltags[, N := .N, by = tag]
alltags <- alltags[N > 1]

alltags[order(tag)]