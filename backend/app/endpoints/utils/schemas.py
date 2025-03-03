from marshmallow import Schema, ValidationError, fields, validates, fields as ma_fields


def camelcase(s):
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class CamelCaseSchema(Schema):
    def on_bind_field(self, field_name: str, field_obj: ma_fields.Field) -> None:
        field_obj.data_key = camelcase(field_obj.data_key or field_name)


class StockSchema(Schema):
    open = fields.Number(required=True)
    close = fields.Number(required=True)
    high = fields.Number(required=True)
    low = fields.Number(required=True)
    volume = fields.Integer(required=True)


class MarketResponseSchema(Schema):
    symbol = fields.Str(required=True)
    name = fields.Str(required=True)
    stocks = fields.List(fields.Nested(StockSchema), required=True)


class MarketRequestSchema(Schema):
    ticker = fields.Str(required=True)
    start_date = fields.Str(required=True)
    end_date = fields.Str(required=True)
    interval = fields.Str(required=True)
