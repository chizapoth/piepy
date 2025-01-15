# Load necessary libraries
library(keras)
library(tensorflow)

# Simulated example data (replace with your own time series)
set.seed(123)
data <- cumsum(rnorm(200))  # Replace with your actual time series data
plot(data)

# Define forecast horizon
forecast_horizon <- 30

# Prepare the data
train_size <- length(data) - 2 * forecast_horizon
val_size <- forecast_horizon # only using 30 as validation
test_size <- forecast_horizon


# Split data into training, validation, and testing sets
train_data <- data[1:train_size]
val_data <- data[(train_size + 1):(train_size + val_size)]
test_data <- data[(train_size + val_size + 1):length(data)]



# Normalize the data (optional, but recommended)
normalize <- function(x) (x - min(x)) / (max(x) - min(x))
# minmax normalization
train_data_norm <- normalize(train_data)
val_data_norm <- normalize(val_data)
test_data_norm <- normalize(test_data)

# Create sequences for LSTM
create_sequences <- function(data, seq_length) {
  # data <- train_data_norm
  
  X <- array(dim = c(length(data) - seq_length, seq_length, 1))
  y <- array(dim = c(length(data) - seq_length, 1))
  for (i in 1:(length(data) - seq_length)) {
    X[i,,1] <- data[i:(i + seq_length - 1)]
    y[i] <- data[i + seq_length]
  }
  list(X = X, y = y)
}


# Sequence length
seq_length <- 10  # Adjust based on your preference

# Prepare sequences
train_sequences <- create_sequences(train_data_norm, seq_length)
val_sequences <- create_sequences(val_data_norm, seq_length)

# Build LSTM model
model <- keras_model_sequential()  |> 
  layer_lstm(units = 50, 
             input_shape = c(seq_length, 1), 
             return_sequences = FALSE)  |> 
  layer_dense(units = 1)

model |>  compile(
  optimizer = "adam",
  loss = "mse"
)

# Train the model
history <- model %>% fit(
  x = train_sequences$X,
  y = train_sequences$y,
  validation_data = list(val_sequences$X, val_sequences$y),
  epochs = 50,
  batch_size = 16,
  verbose = 2
)

# Forecasting the test set
last_train_sequence <- tail(train_data_norm, seq_length)
predicted <- numeric(test_size)

for (i in 1:test_size) {
  input <- array(last_train_sequence, dim = c(1, seq_length, 1))
  prediction <- model %>% predict(input)
  predicted[i] <- prediction
  last_train_sequence <- c(last_train_sequence[-1], prediction)
}

# Denormalize the predictions
denormalize <- function(x, original) (x * (max(original) - min(original))) + min(original)
predicted_denorm <- denormalize(predicted, data)

# Plot the results
plot(data, type = "l", main = "Time Series Forecast with LSTM", col = "blue")
lines((length(data) - test_size + 1):length(data), predicted_denorm, col = "red", lwd = 2)
legend("topright", legend = c("Actual", "Forecast"), col = c("blue", "red"), lty = 1, lwd = 2)
