# This file fetches channel IDs from the channel page of a YouTube channel
from selenium import webdriver
from bs4 import BeautifulSoup as bs
import re

def get_channel_id(channel_url):

    channel_ids = []

    for url in channel_url:

        # Set Chrome webdriver 
        driver = webdriver.Chrome()

        try:
            # Load the channel URL
            driver.get(url)

            # Get the page source after loading is complete
            page_source = driver.page_source

            # Use BeautifulSoup to parse the page source
            soup = bs(page_source, 'html.parser')

            # Find the channel ID in the parsed HTML
            for link in soup.find_all('link', href=re.compile(r'channel/')):
                channel_ids.append(link.get('href').split('channel/')[-1])
                break

        
        finally:
            driver.quit()

    return channel_ids


print(get_channel_id([
    'https://www.youtube.com/@TravisMedia/', 
    'https://www.youtube.com/@turningthetables',
    'https://www.youtube.com/@thisdayinai'
    ]))




