import os
import random
import time
from elevenlabs import play, save
from elevenlabs.client import ElevenLabs
import subprocess
import datetime
from mutagen.mp3 import MP3
import edge_tts
import yaml

config = yaml.safe_load(open('config.yaml').read())

if not config["elevenlabs_api"]:
    raise Exception('Missing ElevenLabs API KEY')



client = ElevenLabs(
  api_key=config["elevenlabs_api"] # Defaults to ELEVEN_API_KEY
)


def get_mp3_length(file_path):


    # Wait for the file to be saved
    while not os.path.exists(file_path):
        time.sleep(0.1)  # Wait for 0.1 seconds before checking again

    audio = MP3(file_path)
    return audio.info.length

def makeTTS(string, imgPath):
    length = 0
    path = imgPath.replace(".png", ".mp3")
    audio = client.generate(
        text=string,
        voice="Adam",
        model="eleven_multilingual_v2"
    )
    save(audio=audio, filename="./" + path)
    return get_mp3_length("./" + path)
    




