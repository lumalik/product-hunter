from playwright.sync_api import sync_playwright
import pickle 
import time
from tqdm import tqdm
import os 

def scrape_product_hunt(year=2019):
    with sync_playwright() as p:
        scrolls = 20
        # Launch the browser
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to the page
        page.goto(f"https://www.producthunt.com/leaderboard/yearly/{year}")
        
        for i in tqdm(range(scrolls)):
            # Scroll to the bottom to load all the content
            page.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)  # Wait for the content to load

        # Select the product elements
        products = page.query_selector_all("xpath=//*[contains(@class, 'styles_titleContainer__')]")
        upvotes = page.query_selector_all("xpath=//*[contains(@class, 'styles_voteCountItem__')]")
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
                
                # Upvotes
                upvotes_element = upvotes[i]
                nr_upvotes = upvotes_element.inner_text() if upvotes_element else 0

                product_data.append({
                    "title": title.strip(),
                    "tagline": tagline.strip(),
                    "link": full_link,
                    "upvotes": nr_upvotes
                })

            except Exception as e:
                import pdb; pdb.set_trace()
                print(e)
                continue

        # Close the browser

        browser.close()

    return product_data


# Run the async function
for year in range(2015, 2024):
    if os.path.exists(f'{year}_producthunt.pickle'):
        continue
    product_info = scrape_product_hunt(year=year)

    with open(f'{year}_producthunt.pickle', 'wb') as handle:
        pickle.dump(product_info, handle, protocol=pickle.HIGHEST_PROTOCOL)

