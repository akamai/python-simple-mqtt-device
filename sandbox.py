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


import uuid
from getpass import getpass

import requests


class SandBox:
    DEFAULT_TOPIC = 'data'

    def __init__(self, config_file=None):
        self.config_file = config_file or 'resources/configuration.txt'
        conf = self.read_config()

        self.client_id = conf['client.id.prefix'] + uuid.uuid4().hex
        self.host = conf['mqtt.host']
        self.topic_prefix = conf['topic.prefix']
        self.token = ''
        self.username = ''

    def authenticate(self, username=None, password=None):
        self.username = username or input('Username: ')
        password = password or getpass('Password: ')

        auth_url = f'https://{self.host}/login'

        jwt_body = {
            'username': self.username,
            'password': password,
            'clientId': self.client_id,
        }
        r = requests.post(auth_url, json=jwt_body)
        response_data = r.json()
        self.token = response_data['token']

    def read_config(self):
        with open(self.config_file) as f:
            configuration = f.readlines()

        conf_dict = {}
        for line in configuration:
            line = line.strip()

            if not line:
                continue

            try:
                key, value = line.split('=')
                key, value = key.strip(), value.strip()
                conf_dict[key] = value
            except ValueError:
                print(f'Warning: failed to parse config line: "{line}"')

        return conf_dict

    def get_topic(self, name=DEFAULT_TOPIC):
        return f'{self.topic_prefix}{name}'
