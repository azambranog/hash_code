library(data.table)
library(parallel)


format_as_table <- function(filename) {
  
  input_file <- file.path('data', filename)
  
  slides <- readLines(input_file)
  
  N <- slides[1]
  slides <- tail(slides, -1)
  
  types <- sapply(as.list(slides), function(x) {gsub('^([^ ]*).*$', '\\1',x[1])})
  n_tags <- sapply(as.list(slides), function(x) {as.numeric(gsub('^([^ ]*) ([^ ]*).*$', '\\2', x[1]))})
  tags <- sapply(as.list(slides), function(x) {tail(strsplit(x, ' ')[[1]], -2)})
  
  data <- data.table(orient = types, n_tags=n_tags, tags=tags)
  data[, slide := .I-1]
  
 
  return(data)
}


expand_tags <- function(data) {
  all_tags <- mclapply(as.list(1:nrow(data)), function(i) {
    x <- data.table(
    slide = data[i, slide], tag = unlist(data[i, tags][[1]])
    )
    return(x)
  }, mc.cores = 3)

  all_tags <- rbindlist(all_tags)

  return(all_tags)
}