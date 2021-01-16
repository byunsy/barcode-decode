"""============================================================================
TITLE: scrape.py
BY   : Sang Yoon Byun
============================================================================"""

import re
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as excn
from selenium.webdriver.common.by import By

# Header information
headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
}

""" ===========================================================================
PROCEDURE:
    get_product
PARAMETERS:
    barcode, a standard barcode number (EAN13 for korean)
PURPOSE:
    accesses koreannet, searches the barcode name, and extracts product name
PRODUCES:
    product_name, name of the product with the input barcode number 
=========================================================================== """
def get_product(barcode):

    # Get URL of interest
    url = "http://koreannet.or.kr/home/hpisSrchGtin.gs1?gtin={}".format(barcode)

    # Get html using requests.get()
    req = requests.get(url, headers=headers)

    # Check for any errors in request responses
    req.raise_for_status()

    # Make some very beautiful soup with the attained html
    soup = BeautifulSoup(req.text, features="html.parser")

    # =========================================================================
    # Find element containing the product name
    title_region = soup.find("div", class_="productTit")
    product = title_region.get_text().strip()

    product_name = product.split("\xa0")[-1].strip()

    return product_name

""" ===========================================================================
PROCEDURE:
    refine_keyword
PARAMETERS:
    product, a product name
PURPOSE:
    deletes seemingly unnecessary words that can potentially prevent 
    optimal search results
PRODUCES:
    product, a refined product name
=========================================================================== """
def refine_keyword(product):
    
    paren = ["[", "(", "{", "_"]
    cutoff = []

    if any(p in product for p in paren):
        for p in paren:
            if p in product:
                cutoff.append(product.index(p))
        
        # only until the first occurrence of a parenthesis
        return product[:min(cutoff)]

    return product

""" ===========================================================================
PROCEDURE:
    search_coupang
PARAMETERS:
    product, a refined product name
PURPOSE:
    accesses coupang, searches the product, and extracts all necessary 
    information about the product 
PRODUCES:
    result, a tuple composed of name, image, price, rating
=========================================================================== """
def search_coupang(product):
    
    # Get URL of interest
    url = "https://www.coupang.com/np/search?component=&q={}".format(product)

    # Get html using requests.get()
    req = requests.get(url, headers=headers)

    # Check for any errors in request responses
    req.raise_for_status()

    # Make some very beautiful soup with the attained html
    soup = BeautifulSoup(req.text, features="html.parser")

    # =========================================================================
    # Check how many checks if there were any hits
    hits = soup.find("p", class_="hit-count")
    if hits:
        hits = int(hits.find_all("strong")[1].get_text())

    # If there are not enough (related) hits on our first try, 
    # then we wait for Coupang to load related items list.
    # - can be done using selenium (it will take some extra time)
    if hits is None or hits >= 20:
        product_list = soup.find("ul", id="productList")

    else:
        # Set pathname for chromedriver executable
        chrome_driver = "C:/Users/SangYoon Byun/chromedriver"

        # Set chrome webdriver
        driver = webdriver.Chrome(chrome_driver)

        # Access the given url
        driver.get(url)

        # Driver waits upto 10 seconds to wait for the specific section to load
        WebDriverWait(driver, 10).until(excn.presence_of_element_located(
            (By.ID, 'productListLKMR')))

        # Make a new soup with Selenium
        src = driver.page_source
        soup = BeautifulSoup(src, features="html.parser")

        # Close
        driver.close()

        product_list = soup.find("ul", id="productListLKMR")

    # Find products, excluding the ads (using regex)
    products = product_list.find_all("li", class_=re.compile("^search-product\s$"))

    results = []

    for item in products[:10]:

        # Find product name
        name = item.find("div", class_="name").get_text()

        # Find product img link
        img_link = item.find("img")['src']

        # Find product price
        price = item.find("strong", class_="price-value").get_text()

        # Find product rating if it exists
        rating = item.find("em", class_="rating")
        if rating:
            rating = rating.get_text()

        item_result = (name, img_link, price, rating)
        results.append(item_result)

    return results
    
"""============================================================================
                                     MAIN
============================================================================"""
def main():

    # product = get_product(8801619044704)
    # product = get_product(8801260210473)
    # product = get_product(8809233836910)
    # product = get_product(8804224218584)
    product = get_product(8802203531235)

    refined = refine_keyword(product)
    print(refined)

    results = search_coupang(refined)
    print(results)

if __name__ == '__main__':
    main()    