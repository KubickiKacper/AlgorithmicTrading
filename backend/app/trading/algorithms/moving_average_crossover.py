def moving_average_crossover(market_data):
    short_window = 10
    long_window = 50

    market_data['Short_MA'] = market_data['Close'].rolling(window=short_window, min_periods=1).mean()
    market_data['Long_MA'] = market_data['Close'].rolling(window=long_window, min_periods=1).mean()

    line_values_dict = {
        'short ma': market_data['Short_MA'].tolist(),
        'long ma': market_data['Long_MA'].tolist()
    }

    signals = []
    for i in range(1, len(market_data)):
        current_short = market_data['Short_MA'].iloc[i]
        current_long = market_data['Long_MA'].iloc[i]
        prev_short = market_data['Short_MA'].iloc[i - 1]
        prev_long = market_data['Long_MA'].iloc[i - 1]

        if prev_short <= prev_long and current_short > current_long:
            signals.append({"x": market_data.index[i].strftime('%Y-%m-%d'), "text": "BUY"})
        elif prev_short >= prev_long and current_short < current_long:
            signals.append({"x": market_data.index[i].strftime('%Y-%m-%d'), "text": "SELL"})

    return line_values_dict, signals
