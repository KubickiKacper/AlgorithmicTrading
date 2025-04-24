import yfinance as yf
import pandas as pd


def get_market_data(ticker, start_date, end_date, interval):
    data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
    return data


def calculate_profit(market_data):
    if market_data.empty:
        return 0.0

    first_close = float(market_data["Close"].iloc[0].item())
    last_close = float(market_data["Close"].iloc[-1].item())

    profit_percentage = ((last_close - first_close) / first_close) * 100
    return round(profit_percentage, 2)


def calculate_algorithm_profit(market_data, signals):
    try:
        if not signals or market_data.empty or "Close" not in market_data.columns:
            print("No signals or invalid market data")
            return 0.0

        market_data = market_data.copy()
        market_data.index = pd.to_datetime(market_data.index)

        current_capital = 1.0
        transactions = []

        i = 0
        while i < len(signals):
            if signals[i]["text"] == "BUY":
                buy_date = pd.to_datetime(signals[i]["x"])
                if i == len(signals) - 1:
                    sell_date = market_data.index[-1]
                    try:
                        if buy_date not in market_data.index:
                            print(f"Missing data: buy_date={buy_date}")
                            break

                        buy_price = float(market_data.loc[buy_date, "Close"].item())
                        sell_price = float(market_data.loc[sell_date, "Close"].item())

                        if buy_price <= 0 or pd.isna(buy_price) or pd.isna(sell_price):
                            print(f"Invalid prices: buy_price={buy_price}, sell_price={sell_price}")
                            break

                        transaction_profit = (sell_price - buy_price) / buy_price
                        current_capital *= (1 + transaction_profit)

                        transactions.append({
                            "buy_date": buy_date.strftime('%Y-%m-%d'),
                            "buy_price": buy_price,
                            "sell_date": sell_date.strftime('%Y-%m-%d'),
                            "sell_price": sell_price,
                            "profit_percentage": round(transaction_profit * 100, 2),
                            "capital_after": round(current_capital, 4)
                        })
                    except KeyError as e:
                        print(f"KeyError: {e} for buy_date={buy_date}, sell_date={sell_date}")
                    break

                for j in range(i + 1, len(signals)):
                    if signals[j]["text"] == "SELL":
                        sell_date = pd.to_datetime(signals[j]["x"])
                        try:
                            if buy_date not in market_data.index or sell_date not in market_data.index:
                                print(f"Missing data: buy_date={buy_date}, sell_date={sell_date}")
                                i = j + 1
                                break

                            buy_price = float(market_data.loc[buy_date, "Close"])
                            sell_price = float(market_data.loc[sell_date, "Close"])

                            if buy_price <= 0 or pd.isna(buy_price) or pd.isna(sell_price):
                                print(f"Invalid prices: buy_price={buy_price}, sell_price={sell_price}")
                                i = j + 1
                                break

                            transaction_profit = (sell_price - buy_price) / buy_price
                            current_capital *= (1 + transaction_profit)

                            transactions.append({
                                "buy_date": buy_date.strftime('%Y-%m-%d'),
                                "buy_price": buy_price,
                                "sell_date": sell_date.strftime('%Y-%m-%d'),
                                "sell_price": sell_price,
                                "profit_percentage": round(transaction_profit * 100, 2),
                                "capital_after": round(current_capital, 4)
                            })

                            i = j + 1
                            break
                        except KeyError as e:
                            print(f"KeyError: {e} for buy_date={buy_date}, sell_date={sell_date}")
                            i = j + 1
                            break
                    else:
                        continue
                else:
                    i += 1
            else:
                i += 1

        if transactions:
            print("Transactions:")
            for t in transactions:
                print(f"Buy {t['buy_date']} at {t['buy_price']}, Sell {t['sell_date']} at {t['sell_price']}, "
                      f"Profit: {t['profit_percentage']}%, Capital: {t['capital_after']}")
        else:
            print("No valid transactions found")

        total_profit_percentage = (current_capital - 1) * 100
        return round(total_profit_percentage, 2)

    except Exception as e:
        print(f"Error calculating algorithm profit: {e}")
        return 0.0
