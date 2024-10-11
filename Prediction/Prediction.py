from tensorflow.keras.models import load_model
import pickle
import numpy as np
import os
from Training import Training

class Prediction:
    def __init__(self):
        pass
    def predict(self, ticker, param):
        if os.path.exists(f'models/{ticker}_{param}.keras') and os.path.exists(f'models/{ticker}_scaler_{param}.pkl') and os.path.exists(f'models/{ticker}_features_{param}.pkl') and os.path.exists(f'models/{ticker}_last_entry_{param}.npy'):
            pass
        else:
            trainer = Training.Training(ticker)
            trainer.training()
        model = load_model(f'models/{ticker}_{param}.keras')
        with open(f'models/{ticker}_scaler_{param}.pkl', 'rb') as file:
            scaler = pickle.load(file)
        with open(f'models/{ticker}_features_{param}.pkl', 'rb') as file:
            n_features = pickle.load(file)
        last_entry_reshaped = np.load(f'models/{ticker}_last_entry_{param}.npy')
        predicted_stock_price = model.predict(last_entry_reshaped)
        predicted_stock_price = scaler.inverse_transform(predicted_stock_price)
        return predicted_stock_price[0][0]