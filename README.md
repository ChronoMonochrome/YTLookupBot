# Telegram YouTube Search Bot (Proof of Concept)

<video src="https://github.com/user-attachments/assets/1831567b-147b-40bd-a3ba-7a57101acbc3" controls="controls" style="max-width: 730px;">
</video>

**Note: This project is a proof of concept and may have limitations or lack advanced features.**

This Telegram bot provides a basic functionality to search for videos on YouTube and returns a list of the top results with thumbnails and inline buttons to directly open the videos.

## Features

* **Basic YouTube Search:** Allows users to search for videos on YouTube using a text query.
* **Optional Result Count:** Users can specify the number of search results (default: 5, max: 50).
* **Thumbnails (Attempted):** Tries to display thumbnails for each video result. Due to potential issues with external image URLs, thumbnail display might not always be successful.
* **Inline Buttons:** Each video result includes an inline button with the video title that opens the video in the user's browser.
* **Basic Error Handling:** Includes rudimentary error handling for common input issues and `yt-dlp` execution.
* **Help Command:** Offers basic usage instructions.

**This is a demonstration of a simple bot and might not be suitable for production use without further development and testing.**

## Usage

1.  Start a chat with the bot on Telegram.
2.  Use the `/search` command followed by your search query.
    * `/search funny cat videos` - Searches for the top 5 "funny cat videos".
    * `/search ai tutorial --count=10` - Searches for the top 10 "ai tutorial" videos.
3.  You can also use the `/help` command to see the usage instructions.

## Prerequisites

* **Python 3.7+**
* **Telegram Bot Token:** Obtainable from BotFather on Telegram.
* **`yt-dlp`:** Command-line YouTube downloader used for fetching search results. Install via pip:
    ```bash
    pip install yt-dlp
    ```
* **Python Libraries:** Install required libraries from `requirements.txt`:
    ```bash
    pip install -r requirements.txt
    ```
    (`requirements.txt` content):
    ```
    aiogram==3.x
    python-dotenv
    aiohttp
    argparse
    ```

## Setup

1.  **Clone (if applicable):**
    ```bash
    git clone <repository_url>
    cd <bot_directory>
    ```
2.  **Install Dependencies:**
    ```bash
	python -m venv venv
	source venv/bin/activate
    pip install -r requirements.txt
    ```
3.  **Configure `.env`:**
    Create `.env` in the project root and add your bot token:
    ```
    BOT_TOKEN=YOUR_ACTUAL_BOT_TOKEN
    ```
4.  **Run the Bot:**
    ```bash
    python bot.py
    ```

## Error Handling

Basic error handling is implemented, but further improvements may be needed for a robust application. Thumbnail display relies on external URLs and might fail.

## Contributing

As this is a proof-of-concept project, contributions are not actively sought at this time. However, feedback and suggestions are welcome.

## License

Licensed under the MIT License
