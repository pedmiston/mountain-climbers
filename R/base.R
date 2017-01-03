library(knitr)

fig_width <- 6
fig_height <- 4

opts_chunk$set(
  echo = FALSE,
  message = FALSE,
  warning = FALSE,
  fig.path = "figs/",
  fig.width = fig_width,
  fig.height = fig_height,
  cache = TRUE,
  cache.path = ".cache/"
)

library(tidyverse)
library(plotly)
library(magrittr)
library(gridExtra)

library(evoteams)
library(crotchet)