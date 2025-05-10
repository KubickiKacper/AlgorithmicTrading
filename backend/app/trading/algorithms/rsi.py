import pandas as pd
import numpy as np


def rsi_based(market_data, first_day_buy=False):
    # Obliczanie RSI
    def calculate_rsi(data, periods=14):
        delta = data['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi

    market_data = market_data.copy()
    market_data['RSI'] = calculate_rsi(market_data)
    line_values_dict = {"rsi": market_data['RSI'].tolist()}

    # Generowanie sygnałów z uwzględnieniem stanu pozycji
    signals = []
    position = first_day_buy  # Początkowy stan pozycji

    for i in range(1, len(market_data)):
        current_rsi = market_data['RSI'].iloc[i]
        prev_rsi = market_data['RSI'].iloc[i - 1]

        # Sygnał kupna (BUY) tylko, jeśli nie mamy pozycji
        if not position and prev_rsi <= 30 and current_rsi > 30 and prev_rsi < current_rsi:
            signals.append({"x": market_data.index[i].strftime('%Y-%m-%d'), "text": "BUY"})
            position = True  # Wchodzimy w pozycję

        # Sygnał sprzedaży (SELL) tylko, jeśli mamy pozycję
        elif position and prev_rsi >= 70 and current_rsi < 70 and prev_rsi > current_rsi:
            signals.append({"x": market_data.index[i].strftime('%Y-%m-%d'), "text": "SELL"})
            position = False  # Wychodzimy z pozycji

    return line_values_dict, signals
