#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time


def scrape():


# In[2]:

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# URL of page to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    time.sleep(5)


# In[4]:


    # Create BeautifulSoup object; parse with 'html.parser'
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


# In[5]:


    # Examine the results, then determine element that contains sought info
    #soup
    #print(soup.prettify())


# In[6]:


    titles = soup.find_all('div',class_="content_title")
    #   print(titles)

    news_title = titles[1].find('a').text
    print(news_title)


# In[7]:


    teasers = soup.find_all('div',class_="article_teaser_body")
    #print(teasers)

    news_p = teasers[0].text
    print(news_p)


# In[8]:


    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    time.sleep(5)


# In[9]:


    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(10)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')


# In[10]:


    #print(soup.prettify())


# In[11]:


    articles = soup.find_all('article')
    #print(articles)
    
    link = articles[0].find('a')
    #print(link)
    


    #img_url = link['data-link']
    img_url = link['data-fancybox-href']


    featured_image_url = "https://www.jpl.nasa.gov" + img_url
    print(featured_image_url)


# In[13]:


    urln = 'https://twitter.com/marswxreport'
    browser.visit(urln)
    time.sleep(5)
    browser.reload()
    time.sleep(5)
# In[14]:

    htmln = browser.html
    #print(htmln)
    time.sleep(5)

    soup = BeautifulSoup(htmln, 'html.parser')
    #soup = BeautifulSoup(html)
    time.sleep(5)


# In[15]:

    #print(soup.prettify())

# In[16]:


    articles = soup.find_all('article')
    #print(articles)

    spans = articles[0].find_all('span')
    #print(spans)

    mars_weather = ' '

    for span in spans:
        #print(span.text)
        if len(span.text) > 70:
          mars_weather = span.text
        
    print(mars_weather) 


# In[17]:


    url = 'https://space-facts.com/mars/'


# In[18]:


    tables = pd.read_html(url)
    tables


# In[19]:


    #type(tables)


# In[20]:


    mars_df = tables[0]
    mars_df.columns = ['Attribute', 'Information']
    mars_df.set_index('Attribute', inplace=True)
    mars_df


# In[21]:


    html_table = mars_df.to_html()
    html_table = html_table.replace('\n', '')
    html_table


# In[59]:


    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": " "},
        {"title": "Cerberus Hemisphere", "img_url": " "},
        {"title": "Schiaparelli Hemisphere", "img_url": " "},
        {"title": "Syrtis Major Hemisphere", "img_url": " "},
    ]   

    for hemi in hemisphere_image_urls:

        url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
        browser.visit(url)
        time.sleep(5)

        browser.click_link_by_partial_text(hemi['title'])
        time.sleep(5)
        #browser.click_link_by_href('#open')
        #time.sleep(5)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        downloads = soup.find_all('div',class_="downloads")
        #print(downloads)

        file_refs = downloads[0].find_all('a')
        file_ref = file_refs[0]
        hemi['img_url'] = file_ref['href']

        print(hemi['img_url'])

    #print(hemisphere_image_urls)


# In[ ]:

    mars_data_dict = {
        "news_title" : news_title,
        "news_p" : news_p,
        "featured_image_url" : featured_image_url,
        "mars_weather" : mars_weather,
        "html_table" : html_table,
        "hemisphere_image_urls" : hemisphere_image_urls
    }
    
    return mars_data_dict
