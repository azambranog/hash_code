source('format_as_tables.R')
library(parallel)

message('####', 'prepare data')
t <- system.time({
                   data <- format_as_table('b_lovely_landscapes.txt')
                 })
print(t)

for (cores in 10:1) {
  message('##' , cores)
  t <- system.time( {
                      all_tags <- mclapply(as.list(1:nrow(data)), function(i) {
                        x <- data.table(
                          slide = data[i, slide], tag = unlist(data[i, tags][[1]])
                        )
                        return(x)
                      }, mc.cores = cores)

                      all_tags <- rbindlist(all_tags)
                    })
  print(t)

}


