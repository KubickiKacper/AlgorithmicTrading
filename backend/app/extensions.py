import os

from flask import render_template
from flask_restx import Api, apidoc

api = Api(
    version=os.getenv("API_VERSION"),
    title=os.getenv("FLASK_TITLE"),
)


@apidoc.apidoc.add_app_template_global
def swagger_static(filename):
    return f"./swaggerui/{filename}"


@api.documentation
def custom_ui():
    return render_template(
        "swagger-ui.html",
        title=api.title,
        specs_url="./swagger.json",
    )
