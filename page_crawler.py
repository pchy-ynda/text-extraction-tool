from bs4 import BeautifulSoup
from collections import deque
from fetcher import fetch_url
from link_extractor import extract_links_from_html

# Function to navigate through the website and extract data
def crawl_website(start_url):
    visited_pages = set()
    queue = deque([start_url])
    pages_data = {}

    while queue:
        current_url = queue.popleft()
        if current_url in visited_pages:
            continue
        
        try:

            # Download HTML of current URL, skip if request fails
            html_content = fetch_url(current_url)
            if not html_content:
                continue

            # Structure text into columns
            soup = BeautifulSoup(html_content, 'html.parser')
            sections = get_sections(soup)

            # KV pair of the specific page
            pages_data[current_url] = sections
            
            # Retrieve internal links, add to queue
            links = extract_links_from_html(html_content, current_url)
            for link in links:
                if link not in visited_pages and link not in queue:
                    queue.append(link)

            visited_pages.add(current_url)
            print(f"Crawled: {current_url} | Found {len(links)} links")
            
        except Exception as e:
            print(f"Error processing URL {current_url}: {e}")
            continue

    return pages_data

# Function to parse headers, descriptions, and CTAs from a page
def get_sections(soup):
    sections =[]

    # Filter out irrelevant tags
    unwanted_tags = ['head', 'script', 'meta', 'style', 'header', 'nav', 'footer']
    for tag in soup(unwanted_tags):
        tag.decompose()

    h_tags = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    for header in h_tags:
        title = header.get_text(strip=True)
        description = []
        cta = []

        # Find next sibling that could be a description
        for sibling in header.find_next_siblings():

            # Break at next header
            if sibling.name in ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                break

            if sibling.name in ['p', 'div', 'span']:
                description.append(sibling.get_text(strip=True))

            if sibling.name == 'a' and 'href' in sibling.attrs:
                cta.append(sibling.get_text(strip=True))
    
        sections.append({
            'title': title,
            'description': ' '.join(description).strip(),
            'cta': cta
        })

    return sections