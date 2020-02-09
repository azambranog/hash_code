library(data.table)

idea_1 <- function(datax, all_tags) {
  data <- copy(datax)
  alltags <- copy(all_tags)

  result <- rep('', nrow(data))
  s <- sample(data[, slide], 1)
  show <- 0

  while(nrow(data) > 0) {
    orient <- data[slide == s, orient]
    tags <- data[slide == s, tags][[1]]

    if(orient == 'V') {

      if (nrow(data[(orient == 'V') & (slide != s)]) == 0) {
        data <- data[slide != s]
        alltags <- alltags[slide != s ]
        if (length(data) == 0){
          break
        } else {
          s <- data[, slide]
          if (length(s) > 1) {
            s <- sample(data[, slide], 1)
          }
          next
        }
      }

      s2 <- data[(orient == 'V') & (slide != s), slide]
      if (length(s2) > 1) {
        s2 <- sample(s2, 1)
      }

      tags2 <- data[slide == s2, tags][[1]]


      data <- data[slide != s2]
      data <- data[slide != s]
      alltags <- alltags[slide != s ]
      alltags <- alltags[slide != s2 ]

      s <- paste(s, s2)
      tags <- union(tags, tags2)
    } else {
      data <- data[slide != s]
      alltags <- alltags[slide != s ]
    }

    show <- show + 1
    result[show] <- s

    if (show %% 100 == 0) {
      message('-', nrow(data))
    }

    if ((nrow(data) == 0)) {
      break
    }


    sx <- alltags[ tag %in% tags, unique(slide)]
    if (length(sx) == 0) {
      s <- data[, slide]
      if (length(s) > 1) {
        s <- sample(data[, slide], 1)
      }
    }else if (length(sx) > 1) {
      s <- sample(sx, 1)
    } else {
      s <- sx
    }

  }

  result <- result[result != '']
  result <- c(length(result), result)

  return(result)


}
