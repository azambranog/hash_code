library(data.table)


vertical_distances <- function(filename) {
  
  input_file <- file.path('data', filename)
  
  slides <- readLines(input_file)
  
  N <- slides[1]
  slides <- tail(slides, -1)
  
  types <- sapply(as.list(slides), function(x) {gsub('^([^ ]*).*$', '\\1',slides[1])})
  n_tags <- sapply(as.list(slides), function(x) {as.numeric(gsub('^([^ ]*) ([^ ]*).*$', '\\2',slides[1]))})
  tags <- sapply(as.list(slides), function(x) {tail(strsplit(x, ' ')[[1]], -2)})
  
  data <- data.table(orient = types, n_tags=n_tags, tags=tags)
  data[, slide := .I-1]
  
  v_slides <- data[orient == 'V']
  
  if(nrow(v_slides)==0) {
    message('NO VERTICAL SLIDES')
    return(0)
  }
  
  result <- data.table(s1=rep(NA, nrow(v_slides)^2), s2 = NA, n1=NA, n2=NA, inter = NA)
  ix <- 0
  for (i in 1:(nrow(v_slides)-1)) {
    for (j in (i+1):nrow(v_slides)) {
      ix <- ix+1
      inter <- length(intersect(v_slides[i, tags][[1]], 
                                v_slides[j, tags][[1]]))
      
      result[ix, s1 := v_slides[i, slide]]
      result[ix, s2 := v_slides[j, slide]]
      result[ix, n1 := v_slides[i, n_tags]]
      result[ix, n2 := v_slides[j, n_tags]]
      result[ix, inter:= inter]
    }
  }
  
  write.table(result, file.path('processes', 'vertical_dists', filename), row.names = F)
}

files <- list.files('data', pattern = 'txt$')
for (f in files){
  message(f)
  vertical_distances(f)
}
