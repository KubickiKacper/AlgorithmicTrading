from flask import request
from flask_restx import Namespace, Resource, fields
from http import HTTPStatus
from app.trading.market import get_market_data
import json

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

        response_data = {
            "series": [
                {
                    "name": ticker,
                    "data": [
                        {
                            "x": row.name.strftime('%Y-%m-%d'),
                            "y": row[["Open", "High", "Low", "Close"]].tolist()
                        }
                        for _, row in market_data.iterrows()
                    ],
                }
            ]
        }

        return response_data, HTTPStatus.OK
