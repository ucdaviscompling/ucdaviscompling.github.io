import os
import asyncio
import threading
import time

print("Downloading and installing requirements...")

os.system('curl https://ollama.com/install.sh | sh')
os.system('pip install ollama')

import ollama

async def run():
    cmd = ['ollama', 'serve']
    print('Starting...')
    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
    )

def run_async_in_thread(loop, coro):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(coro) 
    loop.close()

system_msg = ''
model_name = 'llama3.1:8b'

def gen(user_msg, history=[]):
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

    return ollama.chat(model=model_name, messages=msgs)['message']['content']

new_loop = asyncio.new_event_loop() 

thread = threading.Thread(target=run_async_in_thread, args=(new_loop, run()))
thread.start()
time.sleep(3)

print("Downloading model:", model_name)
ollama.pull(model_name)

print("Preparing model...")
ollama.chat(model=model_name, messages=[{ 'role': 'user','content': 'What is NLP?'}])

print("Ready")

