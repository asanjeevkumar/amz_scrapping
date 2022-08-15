"""Search results on amazon, gets the search result and stores them in CSV

references: https://www.scrapehero.com/tutorial-how-to-scrape-amazon-product-details-using-python-and-selectorlib/
"""
import asyncio
import csv
import os

import aiofiles
import aiohttp
from selectorlib import Extractor

# Create an Extractor by reading from the YAML file
e = Extractor.from_yaml_file('search_products.yml')
MAX_PROCESSOR = 4


async def scrape(url):
    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,'
                  'application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    print("Downloading %s" % url)
    # r = requests.get(url, headers=headers)
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url) as r:
            # Simple check to check if page was blocked (Usually 503)
            if r.status > 500:
                if "To discuss automated access to Amazon data please contact" in r.text:
                    print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
                else:
                    print("Page %s must have been blocked by Amazon as the status code was %d" % (url, r.status))
            print(e.extract(await r.text()))
            # Pass the HTML of the page and create
            return e.extract(await r.text())['products']


async def write_extract_file(output_filename: str, csv_list: list, columns: list):
    """
    Write the extracted content into the file

    output_filename : name of the filename to be stored
    csv_file: list dictionary to be stored
    columns: list of columns names
    """
    try:
        with open(output_filename, "w+") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=columns)
            writer.writeheader()
            writer.writerows(csv_list)
    except FileNotFoundError:
        print("Output file not present", output_filename)
        print("Current dir: ", os.getcwd())
        raise FileNotFoundError


async def search():
    """Search the website for search terms on a file"""
    tasks = []
    products = []
    async with aiofiles.open("search_terms.txt", mode='r') as f:
        searchterms = await f.read()
    for term in searchterms.splitlines():
        tasks.append(scrape(f"https://www.amazon.co.uk/s?k={term}"))
        if len(tasks) % MAX_PROCESSOR == 0:  # running only max parallel process

            for prod in await asyncio.gather(*tasks):  # unpacking list to extend
                products.extend(prod)
            tasks = []  # Resetting task list
    if len(tasks):
        products.extend(await asyncio.gather(*tasks))
    return products


async def main():
    products = await search()
    await write_extract_file("products.csv", products, products[0].keys())

if __name__ == '__main__':
    asyncio.run(main())
