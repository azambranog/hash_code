source('format_as_tables.R')
source('scorer.R')
library(igraph)
library(parallel)

f_score <- function(x, y) {
  tx <- x[[1]]
  ty <- y[[1]]
  
  a <- length(setdiff(tx, ty))
  b <- length(setdiff(ty, tx))
  c <- length(intersect(ty, tx))
  return(min(a,b,c))
}
fast_score <- function(result, data) {
  res <- head(data.table(x=as.numeric(result), y=shift(as.numeric(result), -1)), -1)
  
  res[, tagsx := data[res[, x + 1], tags]]
  res[, tagsy := data[res[, y + 1], tags]]
  res[, score := f_score(tagsx, tagsy), by = seq_len(nrow(res))]
  return(res[, sum(score)])
}


### Build a graph and then do a random walk by using igraph, then remove duplicates in the walk

f <- 'b_lovely_landscapes.txt'

message('##############', f, '###########')
message('###', 'preparing data')
data <- format_as_table(f)
message('###', 'flattening tags')
alltags <- expand_tags(data)

alltags[, N := .N, by =tag]
alltags <- alltags[N >1]

alltags <- alltags[order(tag, slide)]

paired <- alltags[, as.list(slide), by = tag]
paired <- paired[, .N, by = .(V1, V2)][order(N)]

pairs <- copy(paired)

pairs[, pair := paste(V1, V2)]

pp <- pairs[, pair]
pp <- paste(pp, collapse = ' ')

pp <- strsplit(pp, ' ')
pp <- pp[[1]]

gg <- graph(pp, directed = F)
rm(pp)

for (ui in 1:100) {
  s <- as.character(sample(data[, slide], 1))
  w <- random_walk(gg, s, 10000000)
  result <- unique(names(w))
  
  score <- fast_score(result, data)
  message(score)
}




