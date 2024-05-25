import json
import os
import requests
import voice, video, steam_reviews
from pathlib import Path

def main():
    # Fetching posts from r/AskReddit

    appid = input("Please Enter AppId: ")
    print(f"⏱ Processing post: {appid}")

    # Make sure we have not already rendered/uploaded post
    if appid in os.listdir('render'):
        print("❌ Post already processed!")

    # setup 
    folder_path = f"./assets/{appid}"
    Path(folder_path).mkdir(parents=True, exist_ok=True)
    Path("./assets/").mkdir(parents=True, exist_ok=True)

    # getting cover and game name
    print("Fetching game name and downloading cover")
    response = requests.get(f"https://store.steampowered.com/api/appdetails?appids={appid}")
    game_data = response.json().get(str(appid))
    if game_data:
        game_name = game_data["data"]["name"]
        cover_art_url = game_data["data"]["header_image"]
        # Download cover art
        cover_art_path = f"./assets/{appid}/cover.png"
        with open(cover_art_path, 'wb') as cover_art_file:
            cover_art_file.write(requests.get(cover_art_url).content)
    else:
        print("❌ Error Fetching gamedata, make sure the appid is correct")
        return

    #Scraping the post, screenshotting, etc
    print("📸 Screenshotting post...")
    steam_reviews.download_funny_steam_reviews(app_id=appid)


    # # Generate TTS clips for each comment
    print("\n📢 Generating voice clips...",end="",flush=True)
    json_file = open(f"./assets/{appid}/review_data.json", 'r')
    dictList = json.load(json_file)
    # generating audio intro
   
    audio_length = voice.makeTTS(game_name + "--- Funny Steam Reviews.---", f"/assets/{appid}/intro.mp3")
    for dict in dictList:
        audio_length += voice.makeTTS(dict["text"], dict["screenshot_path"])
        if audio_length > 90:
            break
    # Render & Upload
    print("\n🎥 Rendering video...")
    video.render(dictList, appid)

if __name__ == '__main__':
    main()