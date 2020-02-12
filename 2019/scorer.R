scorer <- function(result, data) {
  score <- 0
  
  res <- tail(result, -1)
  
  for (i in 1:(length(res)-1)) {
    
    x <- as.numeric(strsplit(res[i], ' ')[[1]])
    y <- as.numeric(strsplit(res[i+1], ' ')[[1]])
    
    tx <- unique(unlist(data[slide %in% x, tags]))
    ty <- unique(unlist(data[slide %in% y, tags]))
    
    a <- length(setdiff(tx, ty))
    b <- length(setdiff(ty, tx))
    c <- length(intersect(ty, tx))
    score <-score + min(a,b,c)
  }
  
  return(score)
  
}






