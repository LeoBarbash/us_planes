box_plots_best_time <- function(){
  
  library(DBI)
  
  conn <- dbConnect(RSQLite::SQLite(), dbname = '/Users/levbarbash/LSE/LondonProg/Coursework/airline2.db')
  
  sql_col <- c('CRSDepTime', 'DayOfWeek', 'DayOfMonth', 'Month')
  plot_col <- c('Hours', 'Day_of_week', 'Day_of_month', 'Month') 
  
  for (i in 1:4) 
  {
    temp_delay <- dbGetQuery(conn, glue::glue('
    SELECT {sql_col[i]} AS `{sql_col[i]}`, DepDelay AS DepDelay
    FROM ontime
    WHERE ontime.Cancelled = 0 AND ontime.Diverted = 0 AND ontime.DepDelay > 0
    '))
    temp_delay[, 1] <- temp_delay[, 1] %/% (1 + 99 * as.integer(sql_col[i] == 'CRSDepTime'))
    colnames(temp_delay)[1] <- 'x_value'
    boxplot(DepDelay~x_value,
            data=temp_delay,
            outline=FALSE,
            xlab=plot_col[i],
            ylab="Delay (in minutes)",
            col="orange",
            border="brown"
    )
  }
  
  dbDisconnect(conn)
}