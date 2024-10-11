import time
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
from keras.src.layers import Dropout
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM
import nltk
import yfinance as yf
import pickle
from tensorflow.python.keras.callbacks import EarlyStopping

class Training:
    def __init__(self, ticker):
        self.ticker = ticker
        self.param = ['Close', 'Open', 'High', 'Low']
        self.start = datetime(2024, 1, 1)
        self.end = datetime.now()
        self.n_features = 60
        try:
            self.data = yf.download(self.ticker, start=self.start, end=self.end)
            self.scaler = MinMaxScaler(feature_range=(0, 1))
        except ValueError as ve:
            raise Exception('Wrong Ticker Symbol Entered: ', ticker)

    def prepare_data(self, data, n_features):
        X, y = [], []
        for i in range(n_features, len(data)):
            X.append(data[i - n_features:i, 0])
            y.append(data[i, 0])
        return np.array(X), np.array(y)

    def training(self):
        for param in self.param:
            scaled_data = self.scaler.fit_transform(self.data[param].values.reshape(-1, 1))
            X, y = self.prepare_data(scaled_data, self.n_features)
            X = X.reshape(X.shape[0], X.shape[1], 1)

            X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

            model = Sequential()
            model.add(LSTM(units=50, return_sequences=True, input_shape=(self.n_features + 1, 1)))
            model.add(LSTM(units=50))
            model.add(Dense(50))
            model.add(Dropout(rate=0.5))
            model.add(Dense(50))
            model.add(Dropout(rate=0.5))
            model.add(Dense(1))

            model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

            early_stopping_monitor = EarlyStopping(
                monitor='val_loss',
                min_delta=0,
                patience=3,
                verbose=1,
                mode='auto',
                restore_best_weights=True
            )

            history = model.fit(
                X_train, y_train,
                validation_data=(X_val, y_val),
                epochs=100,
                callbacks=[early_stopping_monitor]
            )

            model.save(f'models/{self.ticker}_{param}.keras')
            with open(f'models/{self.ticker}_scaler_{param}.pkl', 'wb') as file:
                pickle.dump(self.scaler, file)
            with open(f'models/{self.ticker}_features_{param}.pkl', 'wb') as file:
                pickle.dump(self.n_features, file)
            last_entry_reshaped = X[-1].reshape(1, self.n_features, 1)
            np.save(f'models/{self.ticker}_last_entry_{param}.npy', last_entry_reshaped)
        time.sleep(5)
        return 1