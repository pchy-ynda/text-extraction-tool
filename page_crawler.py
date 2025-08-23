from bs4 import BeautifulSoup
from urllib.parse import urlparse
from fetcher import fetch_url
from link_extractor import extract_links_from_html
import aiohttp
import asyncio

lang_codes = ['en', 'fr', 'de', 'es', 'it', 'pt', 'ru', 'zh', 'ja']

# Function to detect language based on subdirectory and subdomain cases
def detect_language(url):
    parsed_url = urlparse(url)

    # Case 1: Subdirectory language code
    path_parts = parsed_url.path.strip('/').split('/')
    if path_parts and path_parts in lang_codes:
        return path_parts[0]  # Return the first part as language code
    
    # Case 2: Subdomain language code
    #subdomain = parsed_url.netloc.split('.')[0] if parsed_url.hostname else None
    #if subdomain and len(subdomain) in (2, 3):
    #    return subdomain
    
    # Case 3: No language code found
    return "default"

# Function to navigate through the website and extract data
async def crawl_website(start_url):
    visited_pages = set()
    pages_data = {}

    # BFS queue with (url, depth from start node)
    queue = [(start_url, 0)]

    async with aiohttp.ClientSession() as session:
        while queue:
            # Create tasks for all pages at the current level
            tasks = []
            for url, depth in queue:
                if url not in visited_pages:
                    tasks.append(crawl_page(url, depth, session, visited_pages, pages_data))

            # Run them concurrently
            results = await asyncio.gather(*tasks)

            # Flatten all new links for next level
            queue = []
            for new_links in results:
                if new_links:
                    queue.extend(new_links)
    return pages_data

# Function to crawl a single page and return new links found
async def crawl_page(current_url, depth, session, visited_pages, pages_data):
    html_content = await fetch_url(session, current_url)
    if not html_content:
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    sections = get_sections(soup)

    language = detect_language(current_url)
    if language not in pages_data:
        pages_data[language] = {}
    pages_data[language][current_url] = sections

    links = extract_links_from_html(html_content, current_url)
    visited_pages.add(current_url)

    # Filter out already visited links
    new_links = [(link, depth + 1) for link in links if link not in visited_pages]
    print(f"Crawled: {current_url} | Found {len(new_links)} new links | Lang: {language} | Depth: {depth}")
    return new_links


# Function to linearly parse headers, descriptions, and CTAs from a page
def get_sections(soup):
    sections =[]

    # Empty list if body tag is missing
    if not soup.body:
        return sections

    # Filter out irrelevant tags
    unwanted_tags = ['head', 'script', 'meta', 'style', 'header', 'nav', 'footer']
    for tag in soup.find_all(unwanted_tags):
        tag.decompose()

    current_section = None
    headers = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

    for tag in soup.body.descendants:
        if tag.name in headers:
            if current_section:
                sections.append(current_section)
            current_section = {
                'Title': tag.get_text(strip=True),
                'Description': '',
                'CTA': []
            }

        elif tag.name in ['p', 'div', 'span', 'section'] and tag.get_text(strip=True) and not any (parent.name in headers for parent in tag.parents):
            if current_section:
                # Add text to current section
                current_section['Description'] += ' ' + tag.get_text(strip=True)

            else:
                # Empty header section
                sections.append({
                    'Title': None,
                    'Description': tag.get_text(strip=True),
                    'CTA': []
                })

        elif tag.name == 'a' and 'href' in tag.attrs:
            if current_section:
                # Add CTA to current section
                current_section['CTA'].append(tag.get_text(strip=True))

            else:
                # Empty header section with CTA
                sections.append({
                    'Title': None,
                    'Description': '',
                    'CTA': [tag.get_text(strip=True)]
                })

    if current_section:
        sections.append(current_section)

    return sections