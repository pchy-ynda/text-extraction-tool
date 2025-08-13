import requests

# Function to get response from the URL
def fetch_url(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Raise HTTP error for error status codes        
        return response.text
    
    except requests.exceptions.Timeout:
        print("Request timed out for URL:", url)

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error {response.status_code} occurred for URL {url}")

    except requests.exceptions.RequestException as e:
        print("Failed request to fetch URL:", e)

    return None