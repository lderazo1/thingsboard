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

#Set data from firebase realtime
def set_data_realtime(Firebase,data):
    numpyData = {"array": data.tolist()}
    result = Firebase.post('/sdr/',numpyData)
    print("reference : ",result)

#Listen port 5000 in GNU Radio
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:5000") # connect
socket.setsockopt(zmq.SUBSCRIBE, b'') # subscribe to topic of all

while True:
    if socket.poll(10) != 0: # check if there is a message
        time.sleep(2)
        now = datetime.now()
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        print("Date: ", dt_string)
        msg = socket.recv() # grab
        data = np.frombuffer(msg, dtype=np.float32, count=-1) # (complex64 or float32)
        print("Data type: ",type(data))
        send = data[0:10]
        print("-- Successfully Saved --")
        set_data_realtime(Firebase,send)
        print("***\n")
    else:
        time.sleep(2) # wait 1s and try again
        print("Wait connection, please run gnu radio script \n***")
