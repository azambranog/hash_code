source('format_as_tables.R')
source('scorer.R')
library(igraph)
library(parallel)

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

s <- as.character(sample(data[, slide], 1))
w <- random_walk(gg, s, 10000000)
result <- unique(names(w))
score <- scorer(result, data)
message(score)

s <- as.character(sample(data[, slide], 2))
shortest_paths(gg, s[1], s[2])


