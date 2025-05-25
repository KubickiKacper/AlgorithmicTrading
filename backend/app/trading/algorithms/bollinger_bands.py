import pandas as pd
import numpy as np


def bollinger_bands(market_data, first_day_buy=False):
    # Obliczanie średniej ruchomej (SMA) i odchylenia standardowego
    def calculate_bollinger_bands(data, periods=20, multiplier=2):
        sma = data['Close'].rolling(window=periods).mean()
        std = data['Close'].rolling(window=periods).std()
        upper_band = sma + (multiplier * std)
        lower_band = sma - (multiplier * std)

        # Ręczne budowanie list
        middle_band_list = []
        upper_band_list = []
        lower_band_list = []

        # Iteracja po wartościach z użyciem .values
        for sma_val, upper_val, lower_val in zip(sma.values, upper_band.values, lower_band.values):
            # Sprawdzanie NaN na pojedynczej wartości
            middle_band_list.append(float(sma_val) if not np.isnan(sma_val) else 0.0)
            upper_band_list.append(float(upper_val) if not np.isnan(upper_val) else 0.0)
            lower_band_list.append(float(lower_val) if not np.isnan(lower_val) else 0.0)

        return middle_band_list, upper_band_list, lower_band_list

    market_data = market_data.copy()
    middle_band_list, upper_band_list, lower_band_list = calculate_bollinger_bands(market_data)
    line_values_dict = {
        "middle_band": middle_band_list,
        "upper_band": upper_band_list,
        "lower_band": lower_band_list
    }

    # Generowanie sygnałów z uwzględnieniem stanu pozycji
    signals = []
    position = first_day_buy  # Początkowy stan pozycji

    for i in range(1, len(market_data)):
        # Używamy .item() do uzyskania pojedynczej wartości skalarnej
        current_close = market_data['Close'].iloc[i].item()
        prev_close = market_data['Close'].iloc[i - 1].item()
        current_upper = upper_band_list[i]
        current_lower = lower_band_list[i]
        prev_upper = upper_band_list[i - 1] if i > 1 else current_upper
        prev_lower = lower_band_list[i - 1] if i > 1 else current_lower

        # Sygnał kupna (BUY) - cena bieżąca przecina dolną wstęgę w górę
        if (not position and
                current_close > current_lower and prev_close <= prev_lower and
                current_close > prev_close):
            signals.append({"x": market_data.index[i - 1].strftime('%Y-%m-%d'), "text": "BUY"})
            position = True  # Wchodzimy w pozycję

        # Sygnał sprzedaży (SELL) - cena bieżąca przecina górną wstęgę w dół
        elif (position and
              current_close < current_upper and prev_close >= prev_upper and
              current_close < prev_close):
            signals.append({"x": market_data.index[i - 1].strftime('%Y-%m-%d'), "text": "SELL"})
            position = False  # Wychodzimy z pozycji

    return line_values_dict, signals
