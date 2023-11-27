import autogen
import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
from threading import Event
from django.conf import settings


# At the beginning of your script
config_file_path = settings.BASE_DIR / 'game' / 'services' / 'OAI_CONFIG_LIST.json'

def run_autogen_chat(user_input=None):
    global combined_game_text
    # Load the configuration for the local model
    with open(config_file_path, 'r') as file:
        config_list = json.load(file)

    llm_config = {"config_list": config_list}
    user_proxy = autogen.UserProxyAgent(
        name="User_proxy",
        system_message="A human admin.",
        code_execution_config={"last_n_messages": 0, "work_dir": "groupchat"},
        human_input_mode="ALWAYS"
    )
    friend = autogen.AssistantAgent(
        name="Friend",
        system_message="You are helpful friend, describe the scene we are in and give subtle guidance on what next steps might be advised.",
        llm_config=llm_config,
    )
    artist = autogen.AssistantAgent(
        name="Artist",
        system_message="You are an amazing AI artist, generate a text2img prompt that illustrates the current state of the game. Be creative and expressive visually, this is an adventure game.",
        llm_config=llm_config,
    )

    groupchat = autogen.GroupChat(agents=[user_proxy, friend, artist], messages=[], max_round=3)
    manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)
    
    prompt_message = user_input if user_input else "Let's play an epic text based mystery game. Generate a setting for a text-based adventure game and I will tell you what to do next. Stay on topic and be succinct."
    attempts = 0
    max_attempts = 3
    artist_text = ""

    while attempts < max_attempts:
        user_proxy.initiate_chat(manager, message=prompt_message)
        artist_text = artist.last_message().get('content', '')

        if artist_text:
            break
        else:
            attempts += 1

    combined_game_text = artist_text if artist_text else "Default message for empty response."

    # Run the stable diffusion process
    run_stable_diffusion()

    return combined_game_text


def run_stable_diffusion():
    global combined_game_text  # Declare as global to access it
    url = "http://127.0.0.1:7860"

    payload = {
        "prompt": combined_game_text,  # Use the global variable
        "steps": 50
    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)

    r = response.json()

    for i in r['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",",1)[0])))

        png_payload = {
            "image": "data:image/png;base64," + i
        }
        response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)

        pnginfo = PngImagePlugin.PngInfo()
        pnginfo.add_text("parameters", response2.json().get("info"))
        image.save('media/output.png', pnginfo=pnginfo)
        