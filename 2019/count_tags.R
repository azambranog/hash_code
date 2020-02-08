library(data.table)


get_counts <- function(filename) {
  
  input_file <- file.path('data', filename)
  
  slides <- readLines(input_file)
  
  N <- slides[1]
  slides <- tail(slides, -1)
  
  
  tags <- sapply(as.list(slides), function(x) {tail(strsplit(x, ' ')[[1]], -2)})
  
  counts <- table(unlist(tags))
  
  counts <- as.data.table(counts)
  setnames(counts, 'V1', 'tag')
  
  counts[order(N, decreasing = T)]
  
  write.table(counts, file.path('processed', 'counts', filename), row.names = F)
}

files <- list.files('data', pattern = 'txt$')
for (f in files){
  message(f)
  get_counts(f)
}
