import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, LSTM, Input
from tensorflow.keras.models import Model

def pp():
    return accuracy,predicted_price[0], compName, dateu

compName = input("ENTER COMPANY_NAME.CSV : ")
dateu = input("ENTER DATE (XX-MM-YYYY) : ")

#i Load the data
apd = pd.read_csv(compName)
apd.dropna(inplace=True)
apd.pop('Adj Close')
apd.pop('VWAP')

# Select features
features = ['Open', 'High', 'Low', 'Close']

# Scale the data
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(apd[features])

# Define sequence length
sequence_length = 10
X, y = [], []

# Prepare data for training
for i in range(len(scaled_data) - sequence_length):
    X.append(scaled_data[i: i + sequence_length, :])
    y.append(scaled_data[i + sequence_length, 3])

X, y = np.array(X), np.array(y)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define the model architecture
inputs = Input(shape=(X_train.shape[1], X_train.shape[2]))
x = LSTM(50, return_sequences=True)(inputs)
x = LSTM(50, return_sequences=False)(x)
outputs = Dense(1, activation='linear')(x)

# Compile the model
model = Model(inputs=inputs, outputs=outputs)
model.compile(optimizer='adam', loss='mean_squared_error')

# Train the model
model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=2)

# Evaluate the model
loss = model.evaluate(X_test, y_test)
print(f'Mean Squared Error on Test Set: {loss}')


predictions = model.predict(X)


scaled_predictions = np.column_stack((np.zeros((len(predictions), 3)), predictions))
predictions = scaler.inverse_transform(scaled_predictions)[:, 3]

accuracy = (1 - np.abs((apd['Close'][sequence_length:] - predictions) / apd['Close'][sequence_length:]).mean()) * 100
print(f'Accuracy: {accuracy}')



plt.figure(figsize=(12, 6))
plt.plot(apd.index[sequence_length:], apd['Close'][sequence_length:], label='Actual Close Price', color='blue')
plt.plot(apd.index[sequence_length:], predictions, label='Predicted Close Price', color='red')
plt.title('Actual vs Predicted Close Price')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.show()
# Train the model
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=2)


plt.figure(figsize=(10, 6))
plt.plot(history.history['loss'], label='Training Loss')
plt.plot(history.history['val_loss'], label='Validation Loss')
plt.title('Model Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.legend()
plt.show()

# Evaluate the model
loss = model.evaluate(X_test, y_test)
print(f'Mean Squared Error on Test Set: {loss}')

# Today's example
today_open = 150.0
today_high = 155.0
today_low = 148.0
today_close = 152.0
today_date = dateu

# Scale today's data
scaled_today = scaler.transform([[today_open, today_high, today_low, today_close]])

# Create sequence of last 10 days' data
last_10_days = scaled_data[-sequence_length:]
sequence = np.append(last_10_days[1:], scaled_today, axis=0)

# Reshape the sequence for model input
sequence = sequence.reshape(1, sequence.shape[0], sequence.shape[1])

# Predict tomorrow's closing price
predicted_scaled_price = model.predict(sequence)

# Inverse scale the predicted price
predicted_price = scaler.inverse_transform(np.column_stack((np.zeros((len(predicted_scaled_price), 3)), predicted_scaled_price)))[:, 3]

print(f"Predicted closing price for {today_date}: {predicted_price[0]}")

