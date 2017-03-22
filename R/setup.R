# ---- setup
library(tidyverse)
library(plotly)
library(magrittr)
library(gridExtra)

library(mountainclimbers)
library(totems)
library(crotchet)

library(RColorBrewer)
base_theme <- theme_minimal()

theme_colors <- brewer.pal(4, "Set2")
names(theme_colors) <- c("green", "orange", "blue", "pink")
get_theme_color_values <- function(names) theme_colors[names] %>% unname()

scale_color_strategy <- scale_color_manual(
  "strategy",
  labels = c("diachronic", "synchronic"),
  values = get_theme_color_values(c("blue", "green"))
)
scale_fill_strategy <- scale_fill_manual(
  "strategy",
  labels = c("diachronic", "synchronic"),
  values = get_theme_color_values(c("blue", "green"))
)

scale_color_team_label <- scale_color_manual(
  "skill overlap",
  labels = c("4 disjoint", "3", "2 overlapping", "1", "0 identical"),
  values = brewer.pal(7, "BuGn")[7:3]
)
scale_alpha_team <- scale_alpha_discrete(
  "skill overlap",
  labels = c("4 disjoint", "3", "2 overlapping", "1", "0 identical"),
  range = c(1.0, 0.3)
)

scale_y_fitness_pct <- scale_y_continuous("fitness", labels = scales::percent)
scale_x_strategy_rev <- scale_x_discrete("strategy", labels = c("synchronic", "diachronic"))
