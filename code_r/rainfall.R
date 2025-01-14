# do the analysis in R

project_path <- '/Users/chizhang/Documents/GitHub/piepy/'
path <- 'data/Rainfall_data.csv'

rainfall <- read.csv(paste0(project_path, path))
head(rainfall)

# create the datetime variable
rainfall$timestamp <- paste0(
  rainfall$Year, '-', rainfall$Month, '-', rainfall$Day
)
rainfall

class(rainfall$timestamp) # character

# as date
time <- lubridate::as_date(rainfall$timestamp)
class(time)

rainfall$timestamp <- time
# check data types
str(rainfall)


# visualize temperature -----
library(ggplot2)
p <- ggplot(data = rainfall, aes(x = timestamp, y = Temperature))
p <- p + geom_line()
p





