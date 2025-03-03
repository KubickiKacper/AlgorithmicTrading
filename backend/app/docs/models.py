from flask_restx import fields

from app.extensions import api

GET_market = api.model("GET_market", {"ticker": fields.String, "start_date": fields.String, "end_date": fields.String,
                                      "interval": fields.String})
