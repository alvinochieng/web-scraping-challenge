from splinter import Browser
from bs4 import BeautifulSoup 
import time
import requests
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_data = {}
    
    url = 'https://mars.nasa.gov/news'
    browser.visit(url)
    response = requests.get(url)
    
    time.sleep(2)
    
    html = browser.html
    soup = BeautifulSoup(response.text, "html.parser")
    
    news_title = soup.find('div', class_='content_title').get_text()
    
    news_p = soup.find('div', class_='rollover_description_inner').get_text()
    
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    response = requests.get(url)
    
    time.sleep(2)
    
    mars_weather_tweet = []
    soup = BeautifulSoup(response.text, "html.parser")    
    
    tweets = soup.find_all('div', class_='js-tweet-text-container')
    #twitter = soup.find('p').get_text()
     
    for data in tweets:
        twitter = data.find('p').text
        
        if 'sol' and 'pressure' in twitter:
            mars_weather = twitter
            break
        else:
            pass
    
    mars_weather_tweet.append(twitter)
    
    mars_data = {
        "headline": news_title,
        "paragraph": news_p,
        "weather": mars_weather_tweet
    }    
        
    browser.quit()
    
    return mars_data