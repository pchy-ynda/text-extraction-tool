from bs4 import BeautifulSoup

# Function to extract text from HTML content, saved to csv
def extract_text_from_html(html_content):

    # Construct a BeautifulSoup obj
    soup = BeautifulSoup(html_content, 'html.parser')

    # Remove irrelevant tags and its contents
    unwanted_tags = ['head', 'script', 'meta', 'style', 'header', 'nav', 'footer']
    for tag in unwanted_tags:
        tags = soup.find_all(tag)
        tags.decompose()

    # Extract text
    text = soup.get_text(separator='\n', strip=True)
    return text