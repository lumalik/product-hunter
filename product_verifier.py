from playwright.sync_api import sync_playwright
import csv
import os
from urllib.parse import urlparse
from tqdm import tqdm
import os 

def verify_product(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try: 
            response = page.goto(url, timeout=10000)
            
            # Retrieve the HTTP status code using the status() method
            status_code = response.status if response else 0

            if not status_code in [400, 403, 404, 500]:
                status = "Up"
                url = urlparse(page.url).netloc
            else: 
                status = "Down"
                url = urlparse(page.url).netloc

            # TODO: Add that if it resolves back to producthunt.com, then it's down 
            if url == "www.producthunt.com":
                status = "Down"
        except:
            status = "Down"
        browser.close()
    return url, status

def load_processed_urls(data_path, filename):
    filepath = os.path.join(data_path, filename)
    if not os.path.exists(filepath):
        return set()
    with open(filepath, 'r') as file:
        return set(line.strip() for line in file if line.strip())

def save_processed_url(data_path, filename, url):
    filepath = os.path.join(data_path, filename)

    with open(filepath, 'a') as file:
        file.write(f"{url}\n")

data_path = "data"
processed_urls_file = 'processed_urls.txt'
verified_products_file = 'verified_products.csv'
processed_urls = load_processed_urls(data_path, processed_urls_file)

keys = ["producthunt_url", "resolved_url", "status"]

# Ensure the verified products file has a header if it's new
if not os.path.exists(verified_products_file):
    with open(verified_products_file, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()

# Process each year's product file
for year in range(2015, 2020):
    filename = os.path.join(data_path, f"{year}_producthunt.csv")
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        for product in tqdm(reader):
            producthunt_url = product["external_link"]
            if producthunt_url not in processed_urls:
                resolved_url, status = verify_product(producthunt_url)
                with open(verified_products_file, 'a', newline='') as output_file:
                    dict_writer = csv.DictWriter(output_file, keys)
                    dict_writer.writerow({"producthunt_url":producthunt_url, "resolved_url": resolved_url, "status": status})
                save_processed_url(data_path, processed_urls_file, producthunt_url)

