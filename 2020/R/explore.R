library(data.table)


filesx <- list.files('data', full.names = T)

for (f in filesx) {
  message(f)
  
  
  data <- readLines(f)
  
  
  D <- as.numeric(strsplit(data[1], ' ')[[1]][3])
  
  books <- as.numeric(strsplit(data[2], ' ')[[1]])
  books <- data.table(score = books)
  books[, book := .I -1]
  
  
  
  libs <- tail(data, -2)
  
  
  L <- lapply(as.list(seq(1,length(libs), by = 2)), function(i) {
    libinfo <- as.numeric(strsplit(libs[i], ' ')[[1]])
    libbooks <- data.table(book = as.numeric(strsplit(libs[i+1], ' ')[[1]]))
    libbooks[, lib := (i-1)/2]
    libbooks[, sign := libinfo[2]]
    libbooks[, bpd := libinfo[3]]
    
  })
  
  L <- rbindlist(L)
  
  L <- merge(L, books, by = 'book')
  
  
  
  data <- list(data = L, D = D)
  
  
  ff <- gsub('^(.{1}).*$', '\\1', basename(f))
  saveRDS(data, file.path('clean', paste0(ff, '.rds')))
  
  
  message('DONE FILE')
}

