from urllib.parse import urlparse
import pandas as pd
import re

# Function to extract relative URL from a full URL
def get_relative_url(full_url, base_url):
    return full_url.replace(base_url, '').lstrip('/') or "home"

# Function to clean up sheet names for Excel, with char limit
def name_tab(sheet_name):
    return re.sub(r'[\\/*?:"<>|]', '_', sheet_name)[:31]

# Function to export pages data to an Excel file
def export_to_excel(pages_data, base_url):
    domain = urlparse(base_url).netloc

    for language, lang_pages in pages_data.items():
        file_name = f"{domain}_{language}.xlsx"

        with pd.ExcelWriter(file_name, engine='xlsxwriter') as writer:
            for full_url, sections in lang_pages.items():
                relative_url = get_relative_url(full_url, base_url)

                # Separate sheets in a single file
                df = pd.DataFrame(sections)
                df.to_excel(writer, sheet_name=name_tab(relative_url), index=False)
    print(f"Data exported to {file_name}")