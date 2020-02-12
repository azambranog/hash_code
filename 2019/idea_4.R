source('format_as_tables.R')
source('scorer.R')
library(igraph)
library(parallel)

### Build a graph and then do a random walk naively

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


result <- rep('', nrow(data))
gg2 <- gg
s <- as.character(sample(data[, slide], 1))
for (r in 1:length(result)){
  
  if (r %% 1000 == 0) {
    message(r)
  }
  
  result[r] <- s
  
  if (vcount(gg2) == 0) {
    break
  }
  
  candidates <- names(gg2[s])[gg2[s] != 0]
  if (length(candidates) == 0) {
    candidates <- names(V(gg))
  }
  if (length(candidates) > 1) {
    candidates <- sample(candidates, 1)
  }
  
  gg2 <- gg2 - s
  
  s <- candidates
}

result <- result[result != '']

score <- scorer(result, data)
message(score)

