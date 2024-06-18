# Funny Steam Reviews TikTok Bot

An automatic video bot to scrape funny Steam Reviews and render videos with MoviePY. More features will be added eventually.

[Example](https://streamable.com/rqu38z)

If you encounter any bugs, please report them.


## Prerequisites

- Python 3.x
- `elevenlabs` API key

## Setup Instructions

1. **Clone the Repository**

    ```sh
    git clone https://github.com/yoooby/SteamReviews-TikTok
    cd SteamReviews-TikTok
    ```

2. **Add ElevenLabs API Key**

   go to `config.yaml` in the root directory and add your ElevenLabs API key:

    ```yaml
    elevenlabs_api: YOUR_API_KEY_HERE
    ```

3. **Install Requirements**

    ```sh
    pip3 install -r requirements.txt
    ```

4. **Prepare Background Video**

    Choose a background video (e.g., subway surfers) and move it to the `backgrounds` folder. it will randomly select a video in the folder each time.
5. **Run the Bot**

    Run the main script with Python and provide a Steam ID:

    ```sh
    python3 __main__.py
    ```
