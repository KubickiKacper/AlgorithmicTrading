import pandas as pd
import numpy as np


def bollinger_bands(market_data, first_day_buy=False):
    # Obliczanie średniej ruchomej (SMA) i odchylenia standardowego
    def calculate_bollinger_bands(data, periods=20, multiplier=2):
        sma = data['Close'].rolling(window=periods).mean()
        std = data['Close'].rolling(window=periods).std()
        upper_band = sma + (multiplier * std)
        lower_band = sma - (multiplier * std)

        return sma, upper_band, lower_band

    market_data = market_data.copy()
    middle_band, upper_band, lower_band = calculate_bollinger_bands(market_data)
    line_values_dict = {
        "middle_band": middle_band,
        "upper_band": upper_band,
        "lower_band": lower_band
    }

    # Generowanie sygnałów z uwzględnieniem stanu pozycji
    signals = []
    position = first_day_buy  # Początkowy stan pozycji

    for i in range(1, len(market_data)):
        current_close = market_data['Close'].iloc[i]
        prev_close = market_data['Close'].iloc[i - 1]
        current_upper = upper_band[i]
        current_lower = lower_band[i]
        prev_upper = upper_band[i - 1] if i > 1 else current_upper
        prev_lower = lower_band[i - 1] if i > 1 else current_lower

        # Sygnał kupna (BUY) - cena przecina dolną wstęgę w górę, gdy nie mamy pozycji
        if (not position and
                prev_close <= prev_lower and current_close > current_lower and
                prev_close < current_close):
            signals.append({"x": market_data.index[i].strftime('%Y-%m-%d'), "text": "BUY"})
            position = True  # Wchodzimy w pozycję

        # Sygnał sprzedaży (SELL) - cena przecina górną wstęgę w dół, gdy mamy pozycję
        elif (position and
              prev_close >= prev_upper and current_close < current_upper and
              prev_close > current_close):
            signals.append({"x": market_data.index[i].strftime('%Y-%m-%d'), "text": "SELL"})
            position = False  # Wychodzimy z pozycji

    return line_values_dict, signals
