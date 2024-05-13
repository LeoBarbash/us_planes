logreg_classif <- function(){
  
  library(mlr3)
  library(mlr3learners)
  library(dplyr)
  
  conn <- dbConnect(RSQLite::SQLite(), dbname = '/Users/levbarbash/LSE/LondonProg/Coursework/airline2.db')
  
  ml_data <- dbGetQuery(conn, "
    SELECT Month, DayOfMonth, DayOfWeek, CRSDepTime, 
        DepDelay, CRSArrTime, CRSElapsedTime, Distance,
        planes.year AS year, a1.lat AS OrigLat, a1.long AS OrigLong, a2.lat AS DestLat, a2.long AS DestLong
        FROM ontime
        JOIN planes USING(tailnum)
        JOIN airports AS a1 ON ontime.Origin = a1.iata
        JOIN airports AS a2 ON ontime.Dest = a2.iata
        WHERE ontime.Cancelled = 0 AND ontime.Diverted = 0 AND planes.year != '0000' AND planes.year IS NOT NULL AND planes.year != 'None'
  ")
  dbDisconnect(conn)
  
  ml_data$year <- as.integer(ml_data$year)
  ml_data <- ml_data %>%
    mutate(DepDelay = ifelse(DepDelay < 0, 0, DepDelay))
  ml_data <- ml_data %>%
    mutate(DepDelay = as.integer(as.logical(DepDelay)))
  ml_data$DepDelay <- factor(ml_data$DepDelay)
  n <- nrow(titanic)
  train_set <- sample(n, round(0.5*n))
  test_set <- setdiff(1:n, train_set)
  task <- TaskClassif$new('ontime', backend=ml_data, target = 'DepDelay')
  measure <- msr('classif.ce')
  learner_lr <- lrn("classif.log_reg")
  learner_lr$train(task, row_ids = train_set)
  return(list(learner_lr, learner_lr$predict(task, row_ids = test_set)$score()))
}