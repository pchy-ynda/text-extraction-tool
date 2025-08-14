from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag, urlparse

# Function to extract the internal links within a website, queued for crawler.py
def extract_links_from_html(html_content, base_url):

    # Construct a BeautifulSoup obj, set used to avoid duplicates
    soup = BeautifulSoup(html_content, 'html.parser')
    internal_links = set()
    domain = urlparse(base_url).netloc

    # Find anchor tags with href attributes, filter out irrelevant links
    for link in soup.find_all('a', href=True):
        try:
            href = link['href'].strip()

            if (
                href.lower().startswith(('#', 'mailto:', 'javascript:', 'tel:', '')) or
                href.lower().endswith(('.pdf', '.jpg', '.png', '.gif', '.docx', '.xlsx', '.zip'))
                ):
                continue

            abs_url = urljoin(base_url, href)
            abs_url = urldefrag(abs_url)[0]  # Select url attr only

            if urlparse(abs_url).netloc == domain:
                internal_links.add(abs_url)

        except Exception as e:
            print(f"Error processing link '{href}': {e}")
            continue
    return internal_links