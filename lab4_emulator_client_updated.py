
#ENDPOINT
#a2p57ret34yhhu-ats.iot.us-east-2.amazonaws.com

# Import SDK packages
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import time
import json
import pandas as pd
import numpy as np


#TODO 1: modify the following parameters
#Starting and end index, modify this
device_st = 0
device_end = 5

#Path to the dataset, modify this
data_path = "data2/vehicle{}.csv"

#Path to your certificates, modify this
certificate_formatter = "./device{}/dev{}.pem.crt"
key_formatter = "./device{}/dev{}.pem.key"


class MQTTClient:
    def __init__(self, device_id, cert, key):
        # For certificate based connection
        self.device_id = "vehicle"+str(device_id)
        self.state = 0
        self.client = AWSIoTMQTTClient(self.device_id)
        #TODO 2: modify your broker address
        self.client.configureEndpoint("a2p57ret34yhhu-ats.iot.us-east-2.amazonaws.com", 8883)
        self.client.configureCredentials("./device0/rootca.pem", key, cert)
        self.client.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
        self.client.configureDrainingFrequency(2)  # Draining: 2 Hz
        self.client.configureConnectDisconnectTimeout(10)  # 10 sec
        self.client.configureMQTTOperationTimeout(5)  # 5 sec
        self.client.onMessage = self.customOnMessage
        

    def customOnMessage(self,message):
        #TODO3: fill in the function to show your received message
        print("client {} received payload {} from topic {}".format(self.device_id, message.payload, message.topic))


    # Suback callback
    def customSubackCallback(self,mid, data):
        #You don't need to write anything here
        pass


    # Puback callback
    def customPubackCallback(self,mid):
        #You don't need to write anything here
        pass


    def publish(self, n, Payload="fart"):
        #TODO4: fill in this function for your publish
        self.client.subscribeAsync("iot/Vehicle_"+str(n), 0, ackCallback=self.customSubackCallback)
        
        self.client.publishAsync("iot/Vehicle_"+str(n)+"_", Payload, 0, ackCallback=self.customPubackCallback)

    def publish2(self, n, Payload):
        #TODO4: fill in this function for your publish
        self.client.subscribeAsync("iot/Vehicle_"+str(n), 0, ackCallback=self.customSubackCallback)
        
        self.client.publishAsync("iot/Vehicle_"+str(n)+"_", Payload, 0, ackCallback=self.customPubackCallback)



print("Loading vehicle data...")
data = []
for i in range(5):
    a = pd.read_csv(data_path.format(i))
    data.append(a)

print("Initializing MQTTClients...")
clients = []
for device_id in range(device_st, device_end):
    client = MQTTClient(device_id,certificate_formatter.format(device_id,device_id) ,key_formatter.format(device_id,device_id))
    client.client.connect()
    clients.append(client)

counter = 0

maxs = [0,0,0,0,0]

while True:
    time.sleep(0.5)
    for i,c in enumerate(clients):
        time.sleep(0.2)
        data_ = data[i]
        curr_co2 = maxs[i]
        new_co2 = data_["vehicle_CO2"][counter]
        maxs[i] = max(curr_co2, new_co2)
        co2 = maxs[i]

        message = {}
        message["max_co2"] = co2
        message["time_st"] = data_['timestep_time'][counter]
        message["vehicle"] = i

        #c.publish()
        print(i, counter)
        data_ = data[i]
        #message = "Max CO2-"+ str(co2) + "time_stamp-" + str(data_['timestep_time'][counter])+ "vehicle-"+str(i)+".csv"

        c.publish2(n=i, Payload = json.dumps(message))
        #c.publish(n=i, Payload=message)


    counter +=1






