import os
import paho.mqtt.client as mqtt
from pync import Notifier
import json

host = '127.0.0.1'
port = 1890
topic = 'm4/iot/minyak'

def is_json(myjson):
    try:
        json_object = json.loads(myjson)
    except ValueError as e:
        return False
    return True

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(topic)

def on_message(client, userdata, msg):
    if is_json(msg.payload):
        payload = json.loads(msg.payload)
        
        Notifier.notify(
            'Info Minyak Goreng\n'+
            str(payload['price'])+'/'+str(payload['denom'])+'\n'+
            str(payload['status'])+'\n'+
            'Wilayah '+str(payload['province'])+'\n',
            title='IndieOprek',
            activate='com.apple.Safari',
            open='http://dwi.nodered.indieoprek.id/ui/#!/1?socketid=sOusYMU6Leci6Yp9AAAn',
            execute='say "Go to source"',
            appIcon='https://www.tridipi.id/apple-icon-180x180.png',
            sound='default'
        )

    print(msg.topic+": "+str(msg.payload))

client = mqtt.Client("", clean_session=True)
client.on_connect = on_connect
client.on_message = on_message

client.connect(host, port, 60)

client.loop_forever()
