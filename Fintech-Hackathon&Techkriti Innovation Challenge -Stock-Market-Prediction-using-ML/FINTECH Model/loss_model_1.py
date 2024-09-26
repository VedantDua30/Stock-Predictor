import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.layers import Dense, LSTM, Input
from tensorflow.keras.models import Model

# Load the data
apd = pd.read_csv('NESTLE.CSV')
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
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_data=(X_test, y_test), verbose=2)

# Plot the training and validation loss
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
