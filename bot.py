from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from urllib.parse import urlparse, urlunparse
import subprocess
import json
import aiohttp
import asyncio
import argparse

import os
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    print("Error: BOT_TOKEN not found in .env file.")
    exit()

dp = Dispatcher()

def normalize_url(url: str) -> str | None:
    """Normalizes a URL to include a scheme (defaults to https if missing)."""
    parsed_url = urlparse(url)
    if not parsed_url.scheme:
        # If no scheme is present, assume https
        normalized_parts = ('https',) + parsed_url[1:]
        return urlunparse(normalized_parts)
    elif parsed_url.scheme in ('http', 'https'):
        return url
    else:
        # Handle other schemes or invalid cases as needed
        return None
        
async def is_valid_image_url(url: str) -> bool:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url, allow_redirects=True, timeout=5) as response:  # Added timeout
                return response.status == 200 and response.headers.get('Content-Type', '').startswith('image/')
    except aiohttp.ClientError:
        return False
    except asyncio.TimeoutError:
        return False

@dp.message(CommandStart())
async def cmd_start(msg: types.Message) -> None:
    await msg.answer(text='Hello! Use /search to find videos.')

@dp.message(Command(commands=["search"]))
async def cmd_search(message: types.Message) -> None:
    """
    Handles the /search command using argparse for argument parsing.
    Usage: /search [-n COUNT] <query>
    """
    parser = argparse.ArgumentParser(prog="/search", description="Search for videos on YouTube.")
    parser.add_argument("query", nargs="+", help="The search term(s)")
    parser.add_argument("-n", "--count", type=int, default=5, help="Number of videos to search for (default: 5, max: 50)")

    try:
        args = parser.parse_args(message.text.split()[1:])  # Split and exclude the command itself
        query = " ".join(args.query)
        count = min(args.count, 50)  # Enforce maximum count

        if not query:
            await message.answer("Please provide a search query after /search.")
            return
        if not 1 <= count <= 50:
            await message.answer("Invalid video count. Please specify a number between 1 and 50.")
            return

        # Run yt-dlp command
        command = f"yt-dlp ytsearch{count}:\"{query}\" --flat-playlist -j"
        result = await asyncio.create_subprocess_shell(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = await result.communicate()

        if stderr:
            await message.answer(f"Error running yt-dlp: {stderr.decode()}")
            return

        # Parse JSON output and send thumbnail and button for each result
        found_results = False
        for line in stdout.decode().splitlines():
            if line.strip():
                try:
                    json_output = json.loads(line)
                    url = json_output.get("url")
                    title = json_output.get("title", "Video Link")
                    thumbnail_url = json_output.get("thumbnails", [{}])[0].get("url")  # Get the first thumbnail URL

                    if url:
                        builder = InlineKeyboardBuilder()  # Create a new builder for each button
                        builder.add(types.InlineKeyboardButton(text=title, url=url))
                        markup = builder.as_markup()

                        if thumbnail_url:
                            valid_thumbnail_url = normalize_url(thumbnail_url)
                            if valid_thumbnail_url and await is_valid_image_url(valid_thumbnail_url):
                                try:
                                    await bot.send_photo(
                                        message.chat.id,
                                        valid_thumbnail_url,
                                        caption=title,
                                        reply_markup=markup,
                                    )
                                except Exception as e:
                                    print(f"Error sending photo: {e}")
                                    # Don't send anything to the user in case of error
                            else:
                                await message.answer(
                                    f"[{title}]({url})\n(Invalid thumbnail URL)",
                                    parse_mode="Markdown",
                                    reply_markup=markup,
                                )
                        else:
                            await message.answer(
                                f"[{title}]({url})\n(No thumbnail available)",
                                parse_mode="Markdown",
                                reply_markup=markup,
                            )
                        found_results = True
                except json.JSONDecodeError:
                    print(f"Could not decode JSON: {line}")
                    continue

        if not found_results:
            await message.answer("No links found for your search.")

    except Exception as e:
        await message.answer(text=f"An error occurred: {str(e)}")
    
@dp.message(Command(commands=["help"]))
async def cmd_help(message: types.Message) -> None:
    """
    Sends a help message with usage instructions.
    """
    help_text = (
        "Usage: /search [-n COUNT] <query>\n"
        "<query>: The search term(s) (required).\n"
        "-n COUNT, --count COUNT: The number of videos to search for (optional, default=5, max=50)."
    )
    await message.answer(help_text)


async def main() -> None:
    """Entry point"""

    await dp.start_polling(bot)

if __name__ == "__main__":
    bot = Bot(token=BOT_TOKEN)
    asyncio.run(main())