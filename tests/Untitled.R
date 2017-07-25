library(ggplot2)
library(dplyr)
library(magrittr)
library(mountainclimbers)
identical_team <- readr::read_csv("mountainclimbers/data-raw/identical-team.csv")

identical_team %<>%
  recode_strategy() %>%
  extract_position() %>%
  recode_fitness_as_pct()

set.seed(782)
sample_sim_ids <- identical_team %>%
  filter(exp_id == 1) %>%
  group_by(strategy, starting_pos) %>%
  sample_n(1) %>%
  .$sim_id

random_walk_plot <- ggplot(identical_team %>% filter(exp_id == 1)) +
  aes(pos_x, pos_y, group = sim_id, color = strategy) +
  geom_path(alpha = 0.2) +
  annotate("point", x = 0, y = 0, shape = 4) +
  annotate("point", x = -127.3, y = -127.3, shape = 1) +
  coord_equal() +
  facet_wrap("strategy_rev") +
  scale_x_continuous("", labels = NULL) +
  scale_y_continuous("", labels = NULL) +
  scale_color_strategy +
  base_theme +
  theme(legend.position = "none")

random_walk_plot
