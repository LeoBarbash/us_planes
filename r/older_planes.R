box_plots_decade_planes <- function(){
  
  library(DBI)
  
  conn <- dbConnect(RSQLite::SQLite(), dbname = '/Users/levbarbash/LSE/LondonProg/Coursework/airline2.db')
  
  dep_old_planes_delay <- dbGetQuery(conn, "
    SELECT planes.year AS year, DepDelay as DepDelay
    FROM planes JOIN ontime USING(tailnum)
    WHERE ontime.Cancelled = 0 AND ontime.Diverted = 0 AND ontime.DepDelay > 0 AND planes.year != 'None' AND planes.year != '0000' AND planes.year IS NOT NULL
    ")
  dbDisconnect(conn)
  
  decades <- seq(1950, 2000, by = 10)
  
  dep_old_planes_delay$Decade <- cut(
    strtoi(dep_old_planes_delay$year),  
    breaks = c(decades, 2001),           
    labels = paste0(decades, "s"),        
    right = FALSE
  )
  
  boxplot(DepDelay~Decade,
          data=dep_old_planes_delay,
          outline=FALSE,
          xlab='Decade',
          ylab="Delay (in minutes)",
          col="orange",
          border="brown"
  )
  
}