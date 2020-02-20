library(data.table)

doall <- function(f) {
  
  
  data <- readRDS(file.path('clean', paste0(f,'.rds')))
  
  
  D <- data$D
  data <- data$data
  

  
  
  libs <- data[, .(t_score=sum(score), med_score = mean(score), sign_time=min(sign), bpd=min(bpd), tot_books= .N), by = lib]
  libs[, tot_days := tot_books/bpd]
  
  libs[, tm := t_score/max(t_score)]
  libs[ , mx := med_score/max(med_score)]
  libs[, sx := 1-(sign_time/max(sign_time))]
  libs[, bx := bpd/max(bpd)]
  libs[, dx := 1-(tot_days/max(tot_days))]
  
  libs[, rank := .6*t_score + .8*mx + 1*sx + .6*bx + .2*dx]
  
  
  
  libs <- libs[order(rank, decreasing = T)]
  
  libs[, ddd := cumsum(sign_time)]
  libs <- libs[ddd <= (D+1), ]
  
  #keep book where has most value
  #data <- data[data[, .I[score == max(score)], by=book]$V1]
  
  data <- data[lib %in% libs$lib]
  data <- merge(data, libs[, .(lib, ddd)], by = 'lib')  
  data <- data[order(ddd, -score)]
  
  data[, book_order:= 1:.N, by = ddd]
  data[, t:= ddd + book_order]
  #keep book in the lib that comes first
  data[data[, .I[t == min(t)], by=book]$V1]
  
  
  res <- rep('', 2*nrow(libs))
  
  
  for (i in seq(1, length(res), by = 2)) {
    l <- libs[1+((i-1)/2), lib]
    bbs <- data[lib == l, .(book, score)][order(score, decreasing = T), book]
    
    res[i] <- paste(as.character(l), as.character(length(bbs)))
    res[i+1] <- paste(as.character(bbs), collapse= ' ')
  }
  
  res <- c(as.character(length(res)/2), res)
  
  
  writeLines(res, file.path('clean', paste0('idea4_', f, '.txt')))
  
}


for (f in c('a', 'b', 'c', 'e', 'f', 'd')) {
  message('DOING ', f)
  doall(f)
  message('done')
}