library(data.table)


format_as_tables <- function(filename) {
  
  input_file <- file.path('data', filename)
  
  slides <- readLines(input_file)
  
  N <- slides[1]
  slides <- tail(slides, -1)
  
  types <- sapply(as.list(slides), function(x) {gsub('^([^ ]*).*$', '\\1',slides[1])})
  n_tags <- sapply(as.list(slides), function(x) {as.numeric(gsub('^([^ ]*) ([^ ]*).*$', '\\2',slides[1]))})
  tags <- sapply(as.list(slides), function(x) {tail(strsplit(x, ' ')[[1]], -2)[1]})
  
  data <- data.table(orient = types, n_tags=n_tags, tags=tags)
  data[, slide := .I-1]
  
 
  write.table(data[, .(slide, orient, n_tags, tags)], file.path('processed', 'as_tables', filename), row.names = F)
}

files <- list.files('data', pattern = 'txt$')
for (f in files){
  message(f)
  format_as_tables(f)
}
