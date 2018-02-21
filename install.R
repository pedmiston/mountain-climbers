#!/usr/bin/env Rscript
library(devtools)
# Document and install the local package.
# Library names are independent of directory names.
document("data")
install("data")
