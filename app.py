import json
import os
from flask import Flask
from flask_restful import Resource, Api
from apispec import APISpec
from marshmallow import Schema, fields
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from img_loader import loader_app
from colorizer_keras import colorizer_app
from json_parser import json_app

app = Flask(__name__)
api = Api(app)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Colorizer API',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SWAGGER_URL': '/swagger/',
    'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'
})
docs = FlaskApiSpec(app)


class ColorizeResponseSchema(Schema):
    id = fields.Str(default='2ndCYJK')
    title = fields.Str(default='c1f64245afb2')
    url_viewer = fields.Str(default='https://ibb.co/2ndCYJK')
    url = fields.Str(default='https://i.ibb.co/w04Prt6/c1f64245afb2.gif')
    display_url = fields.Str(default='https://i.ibb.co/98W13PY/c1f64245afb2.gif')
    delete_url = fields.Str(default='https://ibb.co/2ndCYJK/670a7e48ddcb85ac340c717a41047e5c')
    success = fields.Str(default='true')
    status = fields.Str(default='200')


class ColorizeRequestSchema(Schema):
    img_url = fields.String(required=True, description="Image link")


class ColorizeAPI(MethodResource, Resource):
    @doc(description='POST Endpoint', tags=['Keras'])
    @use_kwargs(ColorizeRequestSchema, location=('json'))
    @marshal_with(ColorizeResponseSchema)  # marshalling
    def post(self, **kwargs):
        folder_in = "Input"
        folder_out = "Output"
        url = kwargs.get('img_url')
        filename = loader_app.img_download(url)
        net = colorizer_app.load_model()
        colorizer_app.colorize_image(net, folder_in + os.sep + filename, folder_out + os.sep + filename.replace(".", "-out."))
        upload_json = loader_app.img_upload(filename)
        os.remove(folder_in + os.sep + filename)
        os.remove(folder_out + os.sep + filename.replace(".", "-out."))
        result_json = json_app.json_unpack(upload_json)
        return {'id': result_json[0],
                'title': result_json[1],
                'url_viewer': result_json[2],
                'url': result_json[3],
                'display_url': result_json[4],
                'delete_url': result_json[5],
                'success': result_json[6],
                'status': result_json[7]}


api.add_resource(ColorizeAPI, '/color')
docs.register(ColorizeAPI)