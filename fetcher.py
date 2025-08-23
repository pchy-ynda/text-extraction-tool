import aiohttp
import asyncio

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/115.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
}

# Function to get response from the URL
async def fetch_url(session, url):
    try:
        async with session.get(url, timeout=10, headers=HEADERS) as response:
            response.raise_for_status()
            return await response.text()
    
    except asyncio.TimeoutError:
        print("Request timed out for URL:", url)

    except aiohttp.ClientError as e:
        print("Failed request to fetch URL:", url, e)

    return None