from flask import request
from flask_restx import Namespace, Resource, fields
from http import HTTPStatus
from app.trading.market import get_market_data
from app.trading.algorithms.moving_average_crossover import moving_average_crossover

ns = Namespace("market", description="Market Data API")

market_request_model = ns.model("MarketRequest", {
    "ticker": fields.String(required=True, example="AAPL"),
    "start_date": fields.String(required=True, example="2024-02-01"),
    "end_date": fields.String(required=True, example="2024-02-28"),
    "interval": fields.String(required=True, example="1d"),
})


@ns.route("/")
class Market(Resource):
    @ns.expect(market_request_model)
    def post(self):
        data = request.get_json()
        ticker = data.get("ticker", "AAPL")
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        interval = data.get("interval")

        market_data = get_market_data(ticker, start_date, end_date, interval)
        line_values_dict, signals = moving_average_crossover(market_data)

        response_data = []
        for i, (index, row) in enumerate(market_data.iterrows()):
            candle_data = {
                "x": index.strftime('%Y-%m-%d'),
                "y": row[["Open", "High", "Low", "Close"]].tolist(),
            }
            for line_name, line_values in line_values_dict.items():
                candle_data[f"{line_name}_line_value"] = line_values[i]
            response_data.append(candle_data)

        response = {
            "series": [
                {
                    "name": ticker,
                    "data": response_data,
                }
            ],
            "signals": signals
        }

        return response, HTTPStatus.OK
