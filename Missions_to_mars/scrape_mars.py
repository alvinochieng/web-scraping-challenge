from splinter import Browser
from bs4 import BeautifulSoup 
import time
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}
    
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    
    time.sleep(10)
    
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    
    news_title = soup.find('div', class_='image_and_description_container').a.get_text()
    
    news_p = soup.find('div', class_='rollover_description_inner').get_text()
    
    
    mars_data = {
        "headline": news_title,
        "paragraph": news_p
    }
    
    browser.quit()
    
    return mars_data