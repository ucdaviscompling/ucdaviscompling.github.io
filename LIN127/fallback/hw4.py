import time
import os

print("Downloading and installing requirements...")
os.system('pip install ollama')

time.sleep(3)
from ollama import Client
system_msg = ''
model_name = 'llama3.1:8b'
client = None

def init(id):
    global client
    id = id.strip()
    client = Client(host='https://'+id+'.ngrok-free.app')
    print('Initialized')

def gen(user_msg, history=[]):
    if client == None:
        print('Initialize first using hw4a.init(id)\n(replace "id" with the ID provided on canvas)')
        return
    msgs = [{'role': 'system', 'content': system_msg}]
    role = 'user'
    for m in history:
        msgs.append({'role': role, 'content': m})
        if role == 'user':
            role = 'assistant'
        else:
            role = 'user'
    if role != 'user':
        msgs.pop()
        role = 'user'
    msgs.append({'role': role, 'content': user_msg})
    response = client.chat(model=model_name, messages=msgs)['message']['content']

    return response

print("Ready")

