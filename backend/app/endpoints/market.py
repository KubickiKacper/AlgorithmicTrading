from flask import request
from flask_restx import Namespace, Resource, fields
from http import HTTPStatus
import numpy as np
import pandas as pd
from app.trading.market import get_market_data, calculate_profit, calculate_algorithm_profit
from app.trading.algorithms.moving_average_crossover import moving_average_crossover
from app.trading.algorithms.rsi import rsi_based
from app.trading.algorithms.bollinger_bands import bollinger_bands

ns = Namespace("market", description="Market Data API")

market_request_model = ns.model("MarketRequest", {
    "ticker": fields.String(required=True, example="AAPL"),
    "start_date": fields.String(required=True, example="2024-02-01"),
    "end_date": fields.String(required=True, example="2024-02-28"),
    "interval": fields.String(required=True, example="1d"),
    "first_day_buy": fields.Boolean(required=True, example=False),
    "algorithm": fields.String(required=True, example="moving_average"),
})

ALGORITHM_FUNCTIONS = {
    "none": lambda market_data, first_day_buy: ({}, []),
    "MAC": moving_average_crossover,
    "rsi_based": rsi_based,
    "bollinger_bands": bollinger_bands,
}


def handle_algorithm(algorithm_func, market_data, first_day_buy):
    line_values_dict, signals = algorithm_func(market_data, first_day_buy=first_day_buy)
    algorithm_profit = calculate_algorithm_profit(market_data, signals) if algorithm_func != ALGORITHM_FUNCTIONS[
        "none"] else 0
    return line_values_dict, signals, algorithm_profit


@ns.route("/")
class Market(Resource):
    @ns.expect(market_request_model)
    def post(self):
        data = request.get_json()
        ticker = data.get("ticker", "AAPL")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        interval = data.get("interval")
        first_day_buy = data.get("first_day_buy")
        algorithm = data.get("algorithm", "moving_average")

        market_data = get_market_data(ticker, start_date, end_date, interval)
        profit = calculate_profit(market_data)

        algorithm_func = ALGORITHM_FUNCTIONS.get(algorithm, ALGORITHM_FUNCTIONS["none"])
        line_values_dict, signals, algorithm_profit = handle_algorithm(algorithm_func, market_data, first_day_buy)

        # Zabezpieczenie przed NaN i inf w line_values_dict
        for line_name, line_values in line_values_dict.items():
            line_values_dict[line_name] = [
                float(val) if not pd.isna(val) and not np.isinf(val) else 0
                for val in line_values
            ]

        response_data = []
        rsi_data = []
        for i, (index, row) in enumerate(market_data.iterrows()):
            candle_data = {
                "x": index.strftime('%Y-%m-%d'),
                "y": row[["Open", "High", "Low", "Close"]].tolist(),
            }
            # Dodajemy tylko linie inne niż RSI do candle_data
            for line_name, line_values in line_values_dict.items():
                if line_name != "rsi":  # Pomijamy RSI w series
                    candle_data[f"{line_name}_line_value"] = line_values[i]
                # Zapisujemy RSI do osobnej listy
                if line_name == "rsi" and algorithm == "rsi_based":
                    rsi_data.append({
                        "x": index.strftime('%Y-%m-%d'),
                        "y": line_values[i]
                    })
            response_data.append(candle_data)

        # Zabezpieczenie przed NaN i inf w profit i algorithm_profit
        profit = float(profit) if not pd.isna(profit) and not np.isinf(profit) else 0
        algorithm_profit = float(algorithm_profit) if not pd.isna(algorithm_profit) and not np.isinf(
            algorithm_profit) else 0

        response = {
            "series": [
                {
                    "name": ticker,
                    "data": response_data,
                }
            ],
            "signals": signals,
            "profit_percentage": profit,
            "algorithm_profit_percentage": algorithm_profit
        }

        if algorithm == 'rsi_based':
            response["rsi_series"] = [{
                "name": "RSI",
                "data": rsi_data
            }]

        return response, HTTPStatus.OK
