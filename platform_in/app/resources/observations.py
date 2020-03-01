
from flask import jsonify, request
from flask_restful import Resource, Api, reqparse, abort
from datetime import datetime
from app import swagger
from flasgger.utils import swag_from
from app.models import PlatformUser
from app import db
from confluent_kafka import Producer
import json

users = {}

# def validate_post_user(request):
#         validation_status = True
#         result = {}
#         try:
#             data = request.json
#             if not ('username' in data and 'email' in data and 'password' in data):
#                 result = {'status' : "failure",
#                 'data': "Insufficient Data: Username, email, password are required"}
#                 validation_status = False

#         except Exception as e:
#             print(e)
#             result = {'status' : "failure",
#             'data': "Invalid Input, Check JSON schema"}
#             validation_status = False
        
#         response = jsonify(result)
#         response.status_code = 400

#         return validation_status, response

# def db_error_response():
#     result = {'status' : "failure",
#             'data': "Database error"}
#     response = jsonify(result)
#     response.status_code = 400
#     return response

avro_schema = {
    "type": "record",
    "namespace": "com.example",
    "name": "ObservationsPostData",
    "fields": [
        {
            "name": "ObservationBatchId",
            "type": "string"
        },
        {
            "name": "SchemaId",
            "type": "string"
        },
        {
            "name": "ObservationList",
            "type": {
                "type": "array",
                "items":{
                    "name": "Observation",
                    "type": "record",
                    "fields":[
                        {   "name": "observed_value",
                            "type": "int"
                        },
                        {   "name": "observed_time",
                            "type": "string",
                            "logicalType" : "timestamp-micros"
                        }
                    ]
                }
            }
        }
    ]
}

avro_data = { "ObservationsPostData" : {
    "ObservationBatchId" : "batch_id",
    "ObservationSchemaid" : "schema_id",
    "ObservationList" : [
        {"observed_value":10.0},
        {"observed_time":"2018-01-26T12:00:40.930"}
    ]
}

}

class Observation(Resource):

    @swag_from('user.yml')
    def post(self):
        """
        Post new observation
        """
        data = request.get_json()['ObservationsPostData']
        print(data)
        p = Producer({'bootstrap.servers': 'localhost:9092'})
        p.produce('from_python', key=data['ObservationSchemaid'], value=json.dumps(data['ObservationList']))
        p.flush(30)
