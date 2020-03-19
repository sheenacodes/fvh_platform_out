from flask import jsonify, request, Blueprint, current_app
from flask_restful import Resource, Api, reqparse, abort
from datetime import datetime
from app import swagger
from flasgger.utils import swag_from
import json
import os
import redis
from rq import Queue, Connection
from app.tasks import create_task_produce_to_kafka, create_task_push_sentilo_noise_data
from flask_jwt_extended import jwt_required

observations_blueprint = Blueprint("observations", __name__)
api = Api(observations_blueprint)

avro_schema = {
    "type": "record",
    "namespace": "com.example",
    "name": "ObservationsPostData",
    "fields": [
        {"name": "ObservationBatchId", "type": "string"},
        {"name": "SchemaId", "type": "string"},
        {
            "name": "ObservationList",
            "type": {
                "type": "array",
                "items": {
                    "name": "Observation",
                    "type": "record",
                    "fields": [
                        {"name": "observed_value", "type": "int"},
                        {
                            "name": "observed_time",
                            "type": "string",
                            "logicalType": "timestamp-micros",
                        },
                    ],
                },
            },
        },
    ],
}

avro_data = {
    "ObservationsPostData": {
        "ObservationBatchId": "batch_id",
        "ObservationSchemaid": "schema_id",
        "ObservationList": [
            {"observed_value": 10.0},
            {"observed_time": "2018-01-26T12:00:40.930"},
        ],
    }
}


class Observation(Resource):
    # @jwt_required
    @swag_from("apispec/observation.yml")
    def post(self):
        """
        Post new observation
        """
        data = request.get_json()
        print("post observation: ", data)

        with Connection(redis.from_url(current_app.config["REDIS_URL"])):
            q = Queue()
            task = q.enqueue(
                create_task_produce_to_kafka, data, job_timeout=120, result_ttl=120
            )

            response_object = {
                "status": "success",
                "message": {"task_id": task.get_id()},
            }
            return response_object, 202


api.add_resource(Observation, "/observation")


class NoiseObservation(Resource):
    # @jwt_required
    # @swag_from("apispec/observation.yml")
    def put(self):
        """
        Post new observation
        """
        data = request.get_json()
        print("post observation: ", data)

        with Connection(redis.from_url(current_app.config["REDIS_URL"])):
            q = Queue()
            task = q.enqueue(
                create_task_push_sentilo_noise_data, data, job_timeout=120, result_ttl=120
            )

            response_object = {
                "status": "success",
                "message": {"task_id": task.get_id()},
            }
            return response_object, 202


api.add_resource(NoiseObservation, "/cesva/v1")


class TaskStatus(Resource):
    @jwt_required
    @swag_from("apispec/task_status.yml")
    def get(self, task_id):
        with Connection(redis.from_url(current_app.config["REDIS_URL"])):
            q = Queue()
            task = q.fetch_job(task_id)
        if task:
            response_object = {
                "status": "success",
                "message": {
                    "task_id": task.get_id(),
                    "task_status": task.get_status(),
                    "task_result": task.result,
                },
            }
        else:
            response_object = {"status": "error"}
        return jsonify(response_object)


api.add_resource(TaskStatus, "/taskstatus/<task_id>")



# def delivery_report(err, msg):
#     """ Called once for each message produced to indicate delivery result.
#         Triggered by poll() or flush(). """
#     if err is not None:
#         print('Message delivery failed: {}'.format(err))
#     else:
#         print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))



