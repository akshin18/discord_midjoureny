import os
import json
import random
import requests
from config import CHANNEL_ID, HEADERS, GUILD_ID, MIDJOURNERY_ID, SESSION_ID
from img import set_metadata
from storage import Storage



def interaction(guild_id:str, channel_id:str, message_id:str, application_id:str, custom_id:str):
    
    data = {
        "type":3,
        "nonce":nonce(), 
        "guild_id":str(guild_id), 
        "channel_id":str(channel_id), 
        "message_flags":0,
        "message_id":str(message_id), 
        "application_id":str(application_id), 
        "session_id":SESSION_ID,
        "data":{
            "component_type":2,
            "custom_id":str(custom_id) 
        }
        }
    requests.post("https://discord.com/api/v9/interactions", headers=HEADERS, json=data)



def send_message(content:str):
    data = {
        "mobile_network_type":"unknown",
        "content":content,
        "nonce":nonce(),
        "tts":False,
        "flags":0
    }
    requests.post(f"https://discord.com/api/v9/channels/{CHANNEL_ID}/messages", headers=HEADERS, json=data)
    

def send_prompt(prompt):

    url = "https://discord.com/api/v9/interactions"
 
    pre_data = {"type":2,"application_id":f"{MIDJOURNERY_ID}","guild_id":f"{GUILD_ID}","channel_id":f"{CHANNEL_ID}","session_id":f"{SESSION_ID}","data":{"version":"1166847114203123795","id":"938956540159881230","name":"imagine","type":1,"options":[{"type":3,"name":"prompt","value":f"{prompt}"}],"application_command":{"id":"938956540159881230","type":1,"application_id":"936929561302675456","version":"1166847114203123795","name":"imagine","description":"Create images with Midjourney","options":[{"type":3,"name":"prompt","description":"The prompt to imagine","required":True,"description_localized":"The prompt to imagine","name_localized":"prompt"}],"integration_types":[0],"global_popularity_rank":1,"description_localized":"Create images with Midjourney","name_localized":"imagine"},"attachments":[]},"nonce":f"{nonce()}","analytics_location":"slash_ui"}
    payload = {
        'payload_json': json.dumps(pre_data)
        }
    
    requests.post(url, headers=HEADERS, data=payload)



def nonce(k=19):
    return "".join(random.choices("1234567890", k=k))


def get_prompts():
    with open("prompts.txt", "r") as f:
        return [x.strip() for x in f.read().strip().split("\n")]
    


def next_prompt():
    prompt = Storage.prompts.pop(0)
    send_prompt(prompt)

def next_upscale():
    upscale = Storage.to_upscale.pop(0)
    interaction(GUILD_ID, CHANNEL_ID, upscale[0], MIDJOURNERY_ID, upscale[1])


def start():
    Storage.work = True
    Storage.prompts = get_prompts()
    Storage.random_choice = []
    if Storage.prompts != []:
        Storage.state = 1
        next_prompt()
    else:
        print("No Prompts found")

def choose():
    Storage.to_upscale = []
    Storage.state = 2

def get_random_name():
    return "".join(random.choices("1234567890abcdefghijklmnopqrstuvwxyz_", k=25))

def save():
    try:
        os.mkdir("images")
    except:
        pass
    finally:
        images_data = []
        for image_url,img_promt in Storage.to_save_image:
            r = requests.get(image_url)
            name = get_random_name()
            image_path = f"images/{name}.png"
            with open(image_path, "wb") as f:
                f.write(r.content)
            images_data.append([image_path, img_promt])
        set_metadata(images_data)

def auto_choose():
    for message_id,costumn_ids in Storage.random_choice.copy():
        r = random.randint(0,100)
        count = 1
        if r < 70:
            count = 3
        elif r < 82:
            count = 4
        elif r < 91:
            count = 2

        costumn_ids_result = random.choices(costumn_ids, k=count)
        for i in costumn_ids_result:
            Storage.choose.append([message_id,i])
    
def next_choose():
    choose = Storage.choose.pop(0)
    interaction(GUILD_ID, CHANNEL_ID, choose[0], MIDJOURNERY_ID, choose[1])