import requests
from time import time
from uuid import uuid4
import numpy as np
import re
import os
import openai
from time import time,sleep


service_name = 'sensor_simulation'
content_prefix = 'Sensory input scene: '


def get_embedding(payload):  # payload is a list of strings
    # payload example: ['bacon bacon bacon', 'ham ham ham']
    # response example:  [{'string': 'bacon bacon bacon', 'vector': '[1, 1 ... ]'}, {'string': 'ham ham ham', 'vector': '[1, 1 ... ]'}]
    # embedding is already rendered as a JSON-friendly string
    url = 'http://127.0.0.1:999'  # currently the USEv5 service, about 0.02 seconds per transaction!
    response = requests.request(method='POST', url=url, json=payload)
    return response.json()


def nexus_send(payload):  # REQUIRED: content
    url = 'http://127.0.0.1:8888/add'
    payload['time'] = time()
    payload['uuid'] = str(uuid4())
    payload['content'] = content_prefix + payload['content']
    embeddings = get_embedding(list(payload['content']))
    payload['vector'] = embeddings[0]['vector']
    payload['service'] = service_name
    response = requests.request(method='POST', url=url, json=payload)
    print(response.text)


def nexus_search(payload):
    url = 'http://127.0.0.1:8888/search'
    response = requests.request(method='POST', url=url, json=payload)
    return response.json()


def nexus_bound(payload):
    url = 'http://127.0.0.1:8888/bound'
    response = requests.request(method='POST', url=url, json=payload)
    return response.json()


def nexus_save():
    url = 'http://127.0.0.1:8888/save'
    response = requests.request(method='POST', url=url)
    print(response.text)
