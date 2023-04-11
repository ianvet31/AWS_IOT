import json
import logging
import sys
import  platform

from threading import Timer
import greengrasssdk

# Logging
logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

# SDK Client
client = greengrasssdk.client("iot-data")

max_co2 = 0
def lambda_handler(event, context):
    
    curr_co2 = event['message']
    time_st = event['time_stamp']
    vehicle = event['vehicle']

    max_co2 = max(curr_co2, max_co2) 

    client.publish(
        topic = "iot/Vehicle_" + vehicle_val,
        queueFullPolicy="AllOrException",
        payload = json.dumps({"max_co2": max_co2_val, "time_stamp": time_stamp, "vehicle": vehicle_val }),
    )

    return
