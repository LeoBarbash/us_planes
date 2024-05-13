networks_popular_flights <- function(){
  
  library(DBI)
  library(igraph)
  library(dplyr)
  
  conn <- dbConnect(RSQLite::SQLite(), dbname = '/Users/levbarbash/LSE/LondonProg/Coursework/airline2.db')
  
  origin_dest <- list()
  for (year in 2006:2007) {
    query <- glue::glue("
      SELECT Origin AS Origin, Dest AS Dest
      FROM ontime
      WHERE ontime.Cancelled = 0 AND ontime.Diverted = 0 AND ontime.Year = {year}
    ")
    temp_sers <- dbGetQuery(conn, as.character(query))
    
    temp_sers <- temp_sers %>%
      group_by(Origin, Dest) %>%
      summarise(Weight = n()) %>%
      arrange(desc(Weight))
    
    origin_dest[[year - 2006 + 1]] <- temp_sers
  }
  dbDisconnect(conn)
  
  # Merge dataframes
  origin_dest_merged <- inner_join(origin_dest[[1]] %>% head(100), origin_dest[[2]], by = c("Origin", "Dest"))
  origin_dest_merged <- origin_dest_merged %>% 
    rename("Weght2006" = "Weight.x",
           "Weght2007" = "Weight.y")
  
  # Create network graphs
  graphs <- list(graph_from_data_frame(select(origin_dest_merged, Origin, Dest), directed = FALSE), graph_from_data_frame(select(origin_dest_merged, Origin, Dest), directed = FALSE))
  min_weight <- min(origin_dest_merged[,c(3,4)])
  max_weight <- max(origin_dest_merged[,c(3,4)])
  
  for (i in 1:2) {
    g <- graphs[[i]]
    year <- 2006 + i - 1
    weights <- origin_dest_merged[, i+2]
    weightsm <- lapply(weights, function(x) (x - min_weight) / (max_weight - min_weight))
    plot_title <- paste("100 most popular routes in", year)
    
    plot(g, layout = layout.circle(g), edge.color = "blue", edge.width = unlist(weightsm), main = plot_title, vertex.size=0.1)
  }
}