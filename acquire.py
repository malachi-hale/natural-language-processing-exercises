import requests
from bs4 import BeautifulSoup 
import pandas as pd

def get_blog_articles(url):
    '''
    This function will obtain the title and the contents for all the articles mentioned in the exercises above.
    '''
    #Get credentials
    headers = {'User-Agent': 'malachi-hale'}
    #Get url response
    response = requests.get(url, headers=headers)
    html = response.text
    soup = BeautifulSoup(html)
    #Get body div
    body = soup.select(".et_pb_module.et_pb_post_content.et_pb_post_content_0_tb_body")
    #Get title div
    title = soup.select(".et_pb_title_container")
    return {
        "title": title[0].select('h1')[0].text.strip(),
        "contents": body[0].text.strip()     
        }
    

def get_articles(categories):
    '''
    This function will take a list of categories on the news sites and return the top news stories 
    for each of those categories.
    '''
    #User credentials
    headers = {'User-Agent': 'malachi-hale'}
    #Base url
    base = "https://inshorts.com/en/read/"
    #Create a series of empty lists, to which we will append our values
    titles = []
    contents = []
    types = []
    #Loop through the categories
    for category in categories: 
        url = base + category 
        response = requests.get(url, headers=headers)
        html = response.text
        soup = BeautifulSoup(html)
        
        #Get titles
        title = soup.select(".news-card-title.news-right-box")    
        for i in range(0, (len(title))):
            titles.append(title[i].select("[itemprop = 'headline']")[0].text.strip())
        
        #Get body
        body = soup.select(".news-card-content.news-right-box")  
        for i in range(0, (len(body))):
            contents.append(body[i].select('[itemprop="articleBody"]')[0].text.strip())
        
        #Get category
        for i in range(0, len(body)):
            types.append(category)
    
    #Create dataframe of all our lists
    articles =  pd.DataFrame({
        "title": titles, 
        "contents": contents, 
        "category": types
        })  
    
    return articles