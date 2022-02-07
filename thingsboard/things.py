import paho.mqtt.client as paho  # mqtt library
import os
import json
import time
import requests
import datetime
import zmq
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from firebase import firebase

#Initial connection to firebase realtime db
Firebase = firebase.FirebaseApplication('https://link_to_realtime_database.firebasedatabase.app/',None)

#Get data from firebase realtime
def get_data_realtime(Firebase,data):
    data = Firebase.get('sdr','') #name of collection
    b = list(data.items())[-1][1]['array'] #Last record of collection
    return b

ACCESS_TOKEN = 'tokenHERE'  # Token of device looks like WASSsaSASIQWKAS
broker = "localhost"  # host
port = 1883  # port use for mqtt


def update_state(client, userdata, result):  # callback method 
    print("data published to thingsboard \n")
    pass

client1 = paho.Client("default")  # make client object
client1.update_state = subirEstado  # put function in callback level
client1.username_pw_set(ACCESS_TOKEN)  # access token 
client1.connect(broker, port, keepalive=60)  # make connection

while True:
    data = []
    #Source signal
    data = get_data_realtime(Firebase,data)
    for i in data:
        print(i)
        payload = "{"
        payload += "\"Data\":"+str(i);
        payload += "}"
        ret = client1.publish("v1/devices/me/telemetry", payload)  # topic-v1/devices/me/telemetry
        print("***Change status successfully, check in your telemetry tab***")
        print(payload);
        time.sleep(1)
