source('format_as_tables.R')
source('idea_1.R')
source('scorer.R')
library(parallel)

ar <- commandArgs(trailingOnly = TRUE)
f <- ar[2]
itermax <- as.numeric(ar[1])


message('##############', f, '###########')
message('###', 'preparing data')
data <- format_as_table(f)
message('###', 'flattening tags')
all_tags <- expand_tags(data)
message('###', 'loop will start')
for(iter in 1:itermax) {

  if (iter %% 1 == 0) {
    message('#####', iter)
  }
  result <- idea_1(data, all_tags)

  score <- scorer(result, data)

  writeLines(result, file.path('idea_1', gsub('^([^_]*)_.*$', '\\1', f), paste0(score, '.txt')))

}
message('DONE with ', f)
  









