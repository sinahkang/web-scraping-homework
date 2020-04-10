import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from pprint import pprint

def scrape():
    # BASE_URL = "https://mars.nasa.gov/news/"
    # FILE = "html-selenium.txt"
    # FILE_WAIT = "html-selenium-wait.txt"

    # driver = webdriver.Firefox()
    # driver.get(BASE_URL)
    # html = driver.page_source
    # driver.implicitly_wait(10)
    # driver.close()

    # with open(FILE_WAIT, "w+", encoding="utf-8") as f:
    #     f.write(html)
    
    news_url = "https://mars.nasa.gov/news/"
    news_html = requests.get(news_url).text
    news_soup = BeautifulSoup(news_html, "html.parser")

    mars_news_title = news_soup.find("div", class_="content_title").a.text
    mars_news_p = news_soup.find("div", class_="rollover_description_inner").text

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    image_html = requests.get(image_url).text
    image_soup = BeautifulSoup(image_html, "html.parser")

    featured_image_url = image_soup.find("div", class_="img").img["src"]
    mars_image = "https://www.jpl.nasa.gov" + featured_image_url

    weather_url = "https://twitter.com/marswxreport?lang=en"
    weather_html = requests.get(weather_url).text
    weather_soup = BeautifulSoup(weather_html, "html.parser")

    mars_weather = weather_soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text

    facts_url = "http://space-facts.com/mars/"
    facts_html = requests.get(facts_url).text 
    dfs = pd.read_html(facts_html)

    mars_df = dfs[0].rename(columns={0: "description", 1: "value"}).set_index("description")
    mars_facts = mars_df.to_html()

    hemispheres = ["cerberus", "schiaparelli", "syrtis_major", "valles_marineris"]
    mars_hemispheres = [] 

    for hemisphere in hemispheres:
        url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/" + f"{hemisphere}_enhanced"
        html = requests.get(url).text
        soup = BeautifulSoup(html, "html.parser")
        
        img = soup.find("img", class_="wide-image")["src"]
        title = soup.find("h2", class_="title").text
        
        hemispheres_dict = {"title": title, "img_url": "https://astrogeology.usgs.gov" + img}
        
        mars_hemispheres.append(hemispheres_dict)

    data = {"news_title": mars_news_title, 
    "news_content": mars_news_p, 
    "image": mars_image,
    "weather": mars_weather,
    "facts": mars_facts,
    "hemispheres": mars_hemispheres}

    return data 

pprint(scrape())