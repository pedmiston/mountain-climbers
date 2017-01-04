get_experiment_data <- function(experiment) {
  file.path("experiments", paste0(experiment, ".csv")) %>%
    read_csv() %>%
    recode_fitness_as_pct() %>%
    mutate(sim_id = paste(exp_id, sim_id, sep = ":"))
}

recode_fitness_as_pct <- function(frame) {
  mutate(frame, fitness_pct = 1 - fitness/min(fitness))
}

extract_position <- function(frame) {
  pos <- map(frame$pos, jsonlite::fromJSON)
  get_coord <- function(n) {
    map(pos, function(x) x[[n]]) %>%
      unlist()
  }
  frame$pos_x <- get_coord(1)
  frame$pos_y <- get_coord(2)
  frame
}

recode_team <- function(frame) {
  teams <- get_team_info(frame)
  
  # Order teams from most disjoint to least
  team_levels <- letters[5:1]
  team_map <- teams %>%
    select(team, team_id) %>%
    unique() %>%
    arrange(team_id) %>%
    mutate(
      team_label = factor(team_id, levels = team_levels),
      team_label_rev = factor(team_id, levels = rev(team_levels),
                              labels = 0:4)
    )
  
  left_join(frame, team_map)
}

get_team_info <- function(frame) {
  unique(frame$team) %>%
    map(function(team) {
      data <- jsonlite::fromJSON(team)
      data$players %>%
        mutate(
          player = 1:n(),
          team_id = data$name,
          team = team
        )
    }) %>%
    bind_rows()
}

recode_strategy <- function(frame) {
  strategies <- c("diachronic", "synchronic")
  strategy_map <- data_frame(
    strategy = strategies,
    strategy_rev = factor(strategies, levels = rev(strategies))
  )
  left_join(frame, strategy_map)
}