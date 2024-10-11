from StockSentiments.StockSentiments import *
from Prediction.Prediction import Prediction
import numpy as np

class PredictStockPrice:
    def __init__(self, ticker) -> None:
        self.ticker = ticker
        self.params = ['Close', 'Open', 'High', 'Low']
        self.SS = StockSentiments()
        self.F = 1100000000000
        self.I_usa = 500000000000
        self.I_uk = 200000000000
        self.I_jp = 150000000000
        self.I_sing = 100000000000
        self.I_others = 150000000000
        self.P_usa = 0.4545
        self.P_uk = 0.1818
        self.P_jp = 0.1364
        self.P_sing = 0.0909
        self.P_others = 0.1364
        self.map = {}
        self.factor = {
            "Open" : 0.435,
            "High" : 0.3975,
            "Close" : 0.395,
            "Low" : 0.4715
        }
        a, k = (1.5, 0.7)
        adjustment_factor, investment_factor = self.getSentiments()
        self.getPrediction()
        for i in self.map:
            b = self.factor[i]
            PPAF = a * ((1 / (1 + np.exp(-k * adjustment_factor * investment_factor))) * (1 + np.tanh(adjustment_factor * investment_factor))) + b
            self.map[i] = self.map[i]*PPAF

    def getPrediction(self) -> None:
        for param in self.params:
            self.map[param] = Prediction().predict(self.ticker, param)

    def getSentiments(self) -> tuple:
        S_nasdaq, T_nasdaq = self.SS.nasdaq()
        S_nse, T_nse = self.SS.nse()
        S_nikkei, T_nikkei = self.SS.nikkei()
        V_usa = self.SS.usmarkets()
        V_in = self.SS.inmarkets()
        adjustment_factor = ((S_nasdaq + S_nse + S_nikkei) / 3) * ((T_nasdaq + T_nse + T_nikkei) / 3) * ((V_usa + V_in) / 2)
        investment_factor = np.log(self.F) * (((self.I_usa * self.P_usa) + (self.I_uk * self.P_uk) + (self.I_jp * self.P_jp) + (self.I_sing * self.P_sing) + (self.I_others * self.P_others)) / self.F)
        return (adjustment_factor, investment_factor)

if __name__ == "__main__":
    ticker = "ITC.NS"
    ITCNS = PredictStockPrice(ticker)
    for param in ITCNS.map:
        if param == "Open" or param == "Close":
            print(f"Tomorrow {ticker} will {param} at ", ITCNS.map[param])
        else:
            print(f"Tomorrow {ticker} will reach a {param} of ", ITCNS.map[param])