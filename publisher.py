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


from time import sleep

import paho.mqtt.client as mqtt

from sandbox import SandBox


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print(f'Connected with result code {rc}')


sb = SandBox()
sb.authenticate()
topic = sb.get_topic()

client = mqtt.Client(client_id=sb.client_id)
client.on_connect = on_connect
client.username_pw_set(
    username=sb.username,
    password=sb.token
)
client.tls_set()

try:
    client.connect(sb.host, 8883, 60)
    client.loop_start()

    print('Waiting to connect...')
    while not client.is_connected():
        sleep(0.1)

    print('Type blank line or "exit" to quit...')
    while True:
        data = input(f'Enter a message to publish to {topic}: ')
        if not data or data == 'exit':
            break

        client.publish(topic, data, qos=1)
finally:
    client.loop_stop()
    client.disconnect()
