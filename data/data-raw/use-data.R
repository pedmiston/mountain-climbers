library(devtools)
library(tidyverse)
source("R/mountain-climbers.R")

get_experiment_data <- function(experiment) {
  file.path("data-raw", paste0(experiment, ".csv")) %>%
    read_csv() %>%
    recode_fitness_as_pct() %>%
    mutate(sim_id = paste(exp_id, sim_id, sep = ":"))
}

differing_skills <- get_experiment_data("differing-skills") %>%
  extract_position() %>%
  recode_strategy()

same_skills <- get_experiment_data("same-skills") %>%
  extract_position() %>%
  recode_strategy()

use_data(
  differing_skills,
  same_skills,
  overwrite = TRUE
)
