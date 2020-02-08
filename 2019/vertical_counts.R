library(data.table)
source('format_as_tables.R')

files <- list.files('data', pattern = 'txt$')
for (f in files){
  message(f)
  data <- format_as_table(f)
  write.table(data[, .N, by = orient], 
              file.path('processed', 'vertical_counts',f),
              row.names = F)
}