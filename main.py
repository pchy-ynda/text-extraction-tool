from page_crawler import crawl_website
from exporter import export_to_excel
import asyncio

if __name__ == "__main__":
    input_url = input("Enter the website URL to fetch: ").strip()

    pages_data = asyncio.run(crawl_website(input_url))
    export_to_excel(pages_data, input_url)

    print("Website data extraction completed.")