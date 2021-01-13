library(data.table)

doall <- function(f) {
  
  
  data <- readRDS(file.path('clean', paste0(f,'.rds')))
  
  
  D <- data$D
  data <- data$data
  
  #keep book where has most value
  data <- data[data[, .I[score == max(score)], by=book]$V1]
  
  #keep book in the lib with least books
  data[, n_books_lib := .N, by = lib]
  data[data[, .I[n_books_lib == min(n_books_lib)], by=book]$V1]
  
  
  libs <- data[, .(med_score = mean(score), sign_time=min(sign), bpd=min(bpd), tot_books= .N), by = lib]
  libs[, tot_days := tot_books/bpd]
  
  
  libs[ , mx := med_score/max(med_score)]
  libs[, sx := -sign_time/max(sign_time)]
  libs[, bx := bpd/max(bpd)]
  libs[, dx := -tot_days/max(tot_days)]
  
  libs[, rank := 1.4*mx + 1.1*sx + 1.2*bx + 1*dx]
  
  
  
  libs <- libs[order(rank, decreasing = T)]
  
  libs[, ddd := cumsum(sign_time)]
  libs <- libs[ddd <= D, ]
  
  res <- rep('', 2*nrow(libs))
  
  
  for (i in seq(1, length(res), by = 2)) {
    l <- libs[1+((i-1)/2), lib]
    bbs <- data[lib == l, .(book, score)][order(score, decreasing = T), book]
    
    res[i] <- paste(as.character(l), as.character(length(bbs)))
    res[i+1] <- paste(as.character(bbs), collapse= ' ')
  }
  
  res <- c(as.character(length(res)/2), res)
  
  
  writeLines(res, file.path('clean', paste0('idea2_', f, '.txt')))
  
}



for (f in c('a', 'b', 'c', 'e', 'f', 'd')) {
  message('DOING ', f)
  doall(f)
  message('done')
}