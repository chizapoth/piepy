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
p <- ggplot(data = rainfall, aes(x = timestamp, 
                                 y = Precipitation))
p <- p + geom_line()
p


# ___________ ----
# classic TS model ----

# 1. arima ----
library(forecast)

# arima(lh, order = c(1,0,0))

fit1 <- arima(rainfall$Precipitation, 
              order = c(1, 0, 0))
accuracy(fit1)
forecast(fit1, 5)
plot(forecast(fit1, 30))

# does not look like a good fit

# 2. exponential models
# if write NULL instead of F, does not work
# single exponential: model level
fit2 <- HoltWinters(rainfall$Precipitation, 
                    beta = F, 
                    gamma = F)

plot(forecast(fit2, 30))

# double exponential: model level and trend
fit3 <- HoltWinters(rainfall$Precipitation, 
                    gamma = F)

fit3
plot(forecast(fit3, 30))


# triple exponential: level, trend and seasonal
# fit4 <- HoltWinters(rainfall$Precipitation)
# plot(forecast(fit4, 30))








