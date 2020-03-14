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
     
    for data in tweets:
        twitter = data.find('p').text
        
        if 'sol' and 'pressure' in twitter:
            mars_weather = twitter
            break
        else:
            pass
    
    mars_weather_tweet.append(twitter)
    
    url = 'https://space-facts.com/mars'
    browser.visit(url)
    response = requests.get(url)
    
    time.sleep(2)
    
    soup = BeautifulSoup(response.text, 'html.parser')
    
    mars_facts = soup.find('table')
    
    table_rows = mars_facts.find_all('tr')
    
    df_data = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [tr.text for tr in td]
        df_data.append(row)
        scrape_table = pd.DataFrame(df_data, columns=['Description', 'Value'])    
    
        scrape_table.reset_index()
        scrape_table.set_index('Description')
        
        new_scraped = scrape_table.to_html(index=True)
        
        url = 'https://www.jpl.nasa.gov/spaceimages'
        browser.visit(url)
        html = browser.html
        
        time.sleep(2)
        
        soup = BeautifulSoup(html, 'html.parser')
        
        main_page = 'https://www.jpl.nasa.gov'
        
        relative_path = soup.find('div', class_='carousel_items')('article')[0]['style']
        
        get_image_url = relative_path.split("'")
        unclean_image_url = get_image_url[1]
        symbol_removed = unclean_image_url.replace(');', '')
        featured_image_url = main_page + symbol_removed
        
        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        
        time.sleep(2)
        
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        
        hemisphere_image_urls = []
        main_url = 'https://astrogeology.usgs.gov'
        links = soup.find_all('div', class_='item')
        
        for link in links:
            img_url = link.find('a', class_='itemLink product-item')['href']
            title = link.find('h3').text
            final_url = main_url + img_url
            browser.visit(final_url)
            
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            img_wd = soup.find('div', class_='downloads')
            img_link = img_wd.find('a')['href']
            hemisphere_image_urls.append({'title':title, 'image_url':img_link})
            
    mars_data = {
        "headline": news_title,
        "paragraph": news_p,
        "weather": mars_weather_tweet,
        "facts": new_scraped,
        "image": featured_image_url,
        "hemispheres": hemisphere_image_urls
    }    
        
    browser.quit()
    
    return mars_data