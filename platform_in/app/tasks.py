import time
from confluent_kafka import Producer, avro

from flask import current_app

from confluent_kafka.avro import AvroProducer
import json


def delivery_report(err, msg):
    task_status = True
    if err is not None:
        print("Message delivery failed: {}".format(err))
        task_status = False  ## for elk logs
    else:
        print("Message delivered to {} [{}]".format(msg.topic(), msg.partition()))
        task_status = True  ## for elk logs


def create_task_produce_to_kafka(data):

    kafka_producer = Producer(
        {
            "bootstrap.servers": current_app.config["KAFKA_BROKERS"],
            "security.protocol": current_app.config["SECURITY_PROTOCOL"],
            "sasl.mechanism": current_app.config["SASL_MECHANISM"],
            "sasl.username": current_app.config["SASL_UNAME"],
            "sasl.password": current_app.config["SASL_PASSWORD"],
            "ssl.ca.location": current_app.config["CA_CERT"],
        }
    )

    try:
        kafka_producer.produce(
            "test.sputhan.finest.testnoise", json.dumps(data), callback=delivery_report
        )
        print("produce")
        kafka_producer.poll(2)
        if len(kafka_producer) != 0:
            return False
    except BufferError:
        print("local buffer full", len(kafka_producer))
        return False
    except Exception as e:
        print(e)
        return False

    return True


def create_task_produce_avro_to_kafka(data):

    value_schema_str = """
{
   "namespace": "my.test",
   "name": "value",
   "type": "record",
   "fields" : [
     {
       "name" : "name",
       "type" : "string"
     }
   ]
}
"""

    value_schema = avro.loads(value_schema_str)
    value = {"name": "Value"}

    avroProducer = AvroProducer(
        {
            "bootstrap.servers": current_app.config["KAFKA_BROKERS"],
            "security.protocol": current_app.config["SECURITY_PROTOCOL"],
            "sasl.mechanism": current_app.config["SASL_MECHANISM"],
            "sasl.username": current_app.config["SASL_UNAME"],
            "sasl.password": current_app.config["SASL_PASSWORD"],
            "ssl.ca.location": current_app.config["CA_CERT"],
            "on_delivery": delivery_report,
            "schema.registry.url": "https://kafka01.fvh.fi:8081",
        },
        default_value_schema=value_schema,
    )

    try:
        avroProducer.produce(topic="test.sputhan.finest.testnoise", value=value)
        print("avro produce")
        avroProducer.poll(2)
        if len(avroProducer) != 0:
            return False
    except BufferError:
        print("local buffer full", len(avroProducer))
        return False
    except Exception as e:
        print(e)
        return False

    return True


def create_task_push_sentilo_noise_data(data):
    data_streams = data["sensors"]
    topic_prefix = "test.sputhan.finest"

    kafka_producer = Producer(
        {
            "bootstrap.servers": current_app.config["KAFKA_BROKERS"],
            "security.protocol": current_app.config["SECURITY_PROTOCOL"],
            "sasl.mechanism": current_app.config["SASL_MECHANISM"],
            "sasl.username": current_app.config["SASL_UNAME"],
            "sasl.password": current_app.config["SASL_PASSWORD"],
            "ssl.ca.location": current_app.config["CA_CERT"],
        }
    )

    try:
        for data_stream in data_streams:
            topic = data_stream["sensor"]
            observations = data_stream["observations"]
            kafka_producer.produce(
                f"{topic_prefix}.{topic}", json.dumps(observations), callback=delivery_report
            )
            kafka_producer.poll(2)
    except BufferError:
        print("local buffer full", len(kafka_producer))
        return False
    except Exception as e:
        print(e)
        return False

