# python-simple-mqtt-device
#
# Copyright (C) 2020 Akamai Technologies, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Thanks to The Eclipse Paho project team
# Source code home: https://github.com/eclipse/paho.mqtt.python#getting-started


import paho.mqtt.client as mqtt

from sandbox import SandBox


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {rc}')

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(userdata.get_topic())


# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(f'Received message from {msg.topic}: {msg.payload}')


sb = SandBox()
sb.authenticate()


client = mqtt.Client(client_id=sb.client_id, userdata=sb)
client.on_connect = on_connect
client.on_message = on_message
client.username_pw_set(
    username=sb.username,
    password=sb.token
)
client.tls_set()
client.connect(sb.host, 8883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
