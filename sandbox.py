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


import os
import uuid
from getpass import getpass

import requests


class SandBox:
    DEFAULT_TOPIC = 'data'

    def __init__(self, config=None):
        config = config or Config.from_file()

        self.client_id = config.client_id + uuid.uuid4().hex
        self.host = config.host
        self.topic_prefix = config.topic_prefix
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

    def get_topic(self, name=DEFAULT_TOPIC):
        return f'{self.topic_prefix}{name}'


class Config:
    def __init__(self, host, client_id, topic_prefix):
        self.host = host
        self.client_id = client_id
        self.topic_prefix = topic_prefix

    @classmethod
    def from_file(cls, path=None):
        path = path or os.path.join('resources', 'configuration.txt')
        with open(path) as f:
            lines = f.readlines()

        conf_dict = {}
        for line in lines:
            line = line.strip()

            if not line:
                continue

            try:
                key, value = line.split('=')
                key, value = key.strip(), value.strip()
                conf_dict[key] = value
            except ValueError:
                print(f'Warning: failed to parse config line: "{line}"')

        return cls(
            host=conf_dict['mqtt.host'],
            client_id=conf_dict['client.id.prefix'],
            topic_prefix=conf_dict['topic.prefix'],
        )
