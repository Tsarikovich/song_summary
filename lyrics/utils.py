import logging
import os
from typing import Optional
import requests
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from dotenv import load_dotenv

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)
load_dotenv()

MUSIXMATCH_API_KEY = os.getenv("MUSIXMATCH_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not MUSIXMATCH_API_KEY:
    raise ValueError("Missing Musixmatch API key. Set MUSIXMATCH_API_KEY in environment variables.")

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API key. Set OPENAI_API_KEY in environment variables.")


client = OpenAI(api_key=OPENAI_API_KEY)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def fetch_lyrics(artist: str, title: str) -> Optional[str]:
    """
    Fetches the lyrics of a song from the Musixmatch API.

    Args:
        artist (str): The artist's name.
        title (str): The song's title.

    Returns:
        Optional[str]: The song's lyrics or None if not found.
    """
    url = "https://api.musixmatch.com/ws/1.1/matcher.lyrics.get"
    params = {
        "apikey": MUSIXMATCH_API_KEY,
        "q_artist": artist,
        "q_track": title,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data.get("message", {}).get("header", {}).get("status_code") != 200:
            logger.error(f"Musixmatch API returned an error: {data}")
            return None

        return data.get("message", {}).get("body", {}).get("lyrics", {}).get("lyrics_body")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching lyrics: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error in fetch_lyrics: {str(e)}")
        return None

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def summarize_lyrics(lyrics: str) -> str:
    """
    Summarizes the given song lyrics in one sentence using OpenAI's API.

    Args:
        lyrics (str): The song's lyrics.

    Returns:
        str: A summary of the lyrics or an error message if the operation fails.
    """
    if not lyrics:
        return "No lyrics provided."

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes song lyrics."},
                {"role": "user", "content": f"Summarize these song lyrics in one sentence:\n\n{lyrics}"},
            ],
            model="gpt-4",
        )
        return chat_completion.choices[0].message.content.strip()

    except Exception as e:
        logger.error(f"Error summarizing lyrics: {str(e)}")
        return "Error summarizing lyrics."

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
def extract_countries(lyrics: str) -> str:
    """
    Extracts countries mentioned in the song lyrics using OpenAI's API.

    Args:
        lyrics (str): The song's lyrics.

    Returns:
        str: A comma-separated list of countries or an error message if the operation fails.
    """
    if not lyrics:
        return ""

    try:
        prompt = f"List all countries mentioned in the following lyrics: {lyrics}. ONLY COUNTRIES should be mentioned."
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that identifies all countries"
                               "mentioned in song lyrics. You should return list of countries with commas,"
                               "without any additional text. If there were no countries mentioned, return"
                               "empty string. Here are the lyrics. Not cities, not villages, only countries"},
                {"role": "user", "content": prompt}
            ],
            model="gpt-4",
        )
        return chat_completion.choices[0].message.content.strip()

    except Exception as e:
        logger.error(f"Error extracting countries: {str(e)}")
        return ""
