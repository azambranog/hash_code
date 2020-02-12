library(data.table)
source('format_as_tables.R')

## NOT FINISHED


fn <- function(x, y) {
  a <- length(setdiff(x, y))
  b <- length(setdiff(y, x))
  c <- length(intersect(y, x))
  message(a,b,c)
  return(min(a,b,c))

}

datax <- format_as_table('b_lovely_landscapes.txt')


result <- vector('list', nrow(data))
paired <- character(0)

data <- copy(datax)
data[, tags:=lapply(tags, sort)]

for (s in 1:length(result)) {
  
  message(s)
  data[, tag_1 := sapply(tags, function(x) x[1])]
  data <- data[!is.na(tag_1)]
  
  if(nrow(data) == 0)  {
    message('ALL TAGS USED')
    break
  }
  
  result[[s]] <- data[, .(.N, slide), by=tag_1][N >1]
  
  paired <- unique(c(paired, result[[s]][, slide]))
  
  if(length(paired) == nrow(data)) {
    message('ALL PAIRED')
    break
  }
  
  data[!slide %in% paired, tags:=lapply(tags, function(x) tail(x, -1))]
  
}

result <- result[!sapply(result, is.null)]
