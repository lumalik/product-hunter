from playwright.sync_api import sync_playwright
import pickle 
import time
from tqdm import tqdm
import os 
import csv 

def scrape_product_hunt(year=2023):
    with sync_playwright() as p:
        scrolls = 300
        #scrolls = 2
        # Launch the browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to the page
        page.goto(f"https://www.producthunt.com/leaderboard/yearly/{year}")
        
        for i in tqdm(range(scrolls)):
            try:
                # Scroll to the bottom to load all the content
                page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # Wait for the content to load
            except: 
                continue  

        # Select the product elements
        products = page.query_selector_all("xpath=//*[contains(@class, 'styles_titleContainer__')]")
        upvotes = page.query_selector_all("xpath=//*[contains(@class, 'styles_voteCountItem__')]")
        extra_infos = page.query_selector_all("xpath=//*[contains(@class, 'styles_extraInfo__')]")
        external_links = page.query_selector_all("xpath=//*[contains(@class, 'styles_titleContainer__')]/a[2]")
        product_data = []

        print(f"Total products found: {len(products)}")
              
        for i, product in tqdm(enumerate(products)):
            try:
                # Extract the title and tagline
                title_tagline = product.inner_text()
                title, tagline = [title_tagline.split(" — ")[0], " - ".join(title_tagline.split(" — ")[1:])] if " — " in title_tagline else (title_tagline, "")
                
                # Extract the link
                # debug with product.inner_html()
                link_element = product.query_selector("a[href]")
                link = link_element.get_attribute("href") if link_element else ""
                full_link = f"https://www.producthunt.com{link}" if link else ""

                try:
                    extra_info = extra_infos[i].inner_text().split("•")
                    extra_info = [info.replace("\n", "") for info in extra_info]
                    n_comments = extra_info[0]
                    creator = extra_info[1]
                    industry = extra_info[2]
                    product_type = extra_info[3]
                except: 
                    print(f"Error extracting extra info for product {title}")
                    n_comments = 0
                    creator = ""
                    industry = ""
                    product_type = ""

                # get external link to check project status 
                external_link = external_links[i].get_attribute("href")
                external_link = f"https://www.producthunt.com{external_link}"

                # Upvotes
                upvotes_element = upvotes[i]
                nr_upvotes = upvotes_element.inner_text() if upvotes_element else 0

                product_data.append({
                    "title": title.strip(),
                    "tagline": tagline.strip(),
                    "upvotes": nr_upvotes,
                    "number_of_comments": n_comments,
                    "creator": creator,
                    "industry": industry,
                    "product_type": product_type,
                    "link": full_link,
                    "external_link": external_link
                })

            except Exception as e:
                import pdb; pdb.set_trace()
                print(e)
                continue

        # Close the browser
        browser.close()

    return product_data

data_path = "data"

# Run the async function
for year in range(2015, 2020):
    filepath = os.path.join(data_path, f'{year}_producthunt.csv')

    if os.path.exists(filepath):
        continue
    product_info = scrape_product_hunt(year=year)
    
    keys = ["title", "tagline", "upvotes", "number_of_comments", "creator", "industry", "product_type", "link", "external_link"]
    
    with open(filepath, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(product_info)

    print("Scraped a total of {} products for the year {}".format(len(product_info), year))