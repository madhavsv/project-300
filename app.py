from flask import Flask, render_template
import time
from paho.mqtt import client as mqtt_client

app = Flask(__name__)
#Set the Hostname, Port & TopicName
port = 1883
broker = 'broker.emqx.io'
client_id = 'test'
username = 'emqx'
password = ''
topic = 'topicName/pir'
detection = 0
def on_connect(client,user_data,flag,rc):
    client.subscribe(topic)

def on_message(client,user_data,msg):
    global detection
    detection = msg.payload.decode('utf8')

@app.route('/',methods=["GET"])
def connect_mqtt():
    client = mqtt_client.Client(client_id)
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set(username, password)
    client.connect(broker, port)
    client.loop_start()
    for i in range (0,10):
        time.sleep(5)
        print(detection)
        return render_template("index.html",status = int(detection))
    client.loop_stop()
 
if __name__ == '__main__':
    app.run(port=5001)

#https://wokwi.com/projects/367695785453535233
