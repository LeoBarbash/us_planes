tables_delayed_cascade_delays <- function() {
  
  library(DBI)
  
  conn <- dbConnect(RSQLite::SQLite(), dbname = '/Users/levbarbash/LSE/LondonProg/Coursework/airline2.db')
  
  cascade_delay <- dbGetQuery(conn, "
    SELECT Year, Month, DayOfMonth, CRSDepTime, DepTime, DepDelay,
           CRSArrTime, ArrTime, ArrDelay, Origin, Dest, FlightNum
    FROM ontime
    WHERE Cancelled = 0 AND Diverted = 0 AND DepDelay > 0
  ")
  dbDisconnect(conn)
  
  cascade_delay <- cascade_delay[order(-cascade_delay$DepDelay), ]
  origin_flight <- cascade_delay[cascade_delay$DepDelay == quantile(cascade_delay$DepDelay, 0.75), ][1, ]
  
  example <- origin_flight
  delayed_flights <- subset(cascade_delay,
                            Year == example$Year &
                              Month == example$Month &
                              DayofMonth == example$DayofMonth &
                              DepTime > example$ArrTime &
                              CRSDepTime < example$ArrTime &
                              CRSDepTime > example$CRSArrTime &
                              Origin == example$Dest
  )
  
  return(list(origin_flight, delayed_flights))
}