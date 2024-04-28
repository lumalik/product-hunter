# 🦌 Hunting "successful" products on Product Hunt

Ever wondered what makes a product successful on product hunt? 
Or maybe even more interesting - what product on Product Hunt are successful in the real world? 

I want to answer these questions in the following project by scraping products from 2015 to 2019, including the likes on the platform. In a second step I try to access the links to the product websites "today" (26.01.2024) - which is for most products more than 5 years after their Product Hunt launch. "Success" here is defined as being able to reach their website. This approach is prone to errors as some links might be broken but the product might still be operating. Also the domain might have been bought by a competitor.  

If anyone comes up with another scalable approach to assess the "success" of a product, let me know or open up a PR. 

## 1. 🕸 Scraping products on Product Hunt 

From the main directory execute: 

```
python producthunt_scraper.py
```
This results in a dataset of ~12k products from 2015 to 2019. And ~21k products if we include the years up to 2023.

To add the success criterion - in this case whether the site exists, execute: 

```
python product_verifier.py
```

To run with Docker, execute: 

```
docker build -t my-producthunt-scraper .

```

And then 

```
docker run -it my-producthunt-scraper
```

## 2. 👁 Visualizing the data 

TBD 

## 3. 🤖 Training a classifier  

TBD 