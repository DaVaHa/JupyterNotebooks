'''
Test code for Jupyter Notebook

Scraping www.winemag.com for wine ratings.

https://www.winemag.com/?s=&drink_type=beer&page=1

'''
headers = {
    'user-agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                   '(KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36')
}

##import scrapy
##from scrapy.crawler import CrawlerProcess
##
### URL
##url = "http://www.winemag.com/?s=&drink_type=wine&page=1"
##
##results = []
##
##class WineMagSpider( scrapy.Spider ):
##
##    name = 'wine_mag_spider'
##
##    def start_requests( self ):
##        
##        urls = [ "https://www.winemag.com/?s=&drink_type=wine&page=1"]
##        
##        for url in urls:
##            yield scrapy.Request( url = url, callback = self.parse, headers=headers )
##
##    def parse( self, response ):
##
##        # get all reviews from page
##        rankings = response.xpath('//div[@class="review-ranking"]')
##        text = rankings.xpath('./a[@class="review-listing"]/text()')
##        #
##        print(text)
##        
##
##
##
##process = CrawlerProcess()
##process.crawl(WineMagSpider)
##process.start()



from bs4 import BeautifulSoup
import requests
import pandas as pd
import time


startTime = time.time()

main_url = 'https://www.winemag.com/?s=&drink_type=wine&page='

def ScrapeUrl(url):
    
    headers = {
        'user-agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                       '(KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36')
    }

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')

    links = soup.find_all('li', class_="review-item ")

    return links




# function to get extra info
def GetExtraInfo(url):

    r = requests.get(url, headers=headers)
    html = r.text
    soup = BeautifulSoup(html, 'lxml')

    info = soup.find('ul', class_="secondary-info")

    labels = [i.text.strip() for i in info.find_all('div',class_='info-label small-7 columns')]
    values = [v.text.strip() for v in info.find_all('div',class_='info small-9 columns')]

    data = dict(zip(labels,values))
    #print(data)

    return data

    

#GetExtraInfo("https://www.winemag.com/buying-guide/chateau-haut-brion-2016-pessac-leognan-310320/")


def ScrapeFrontPage(links):
    
    results = []

    for link in links:

        scraped_dict = {}
        
        title = link.find('div', class_="title").text
        rating = link.find('span', class_="rating").text
        price = link.find('span', class_="price").text
        #excerpt = link.find('div', class_="excerpt").text
        appellation = link.find('span', class_="appellation").text
        #badge = link.find('span', class_="badge").text
        #print(title, rating, price, appellation)
        href = link.find('a').get('href')

        # front page
        scraped_dict["title"] = title
        scraped_dict["rating"] = rating
        scraped_dict["price"] = price
        scraped_dict["appellation"] = appellation
        scraped_dict["href"] = href

        # secondary
        extra = GetExtraInfo(href)
        if "Alcohol" in extra.keys(): scraped_dict["alcohol"] = extra["Alcohol"]
        if "Category" in extra.keys(): scraped_dict["category"] = extra["Category"]
        if "Date Published" in extra.keys(): scraped_dict["date"] = extra["Date Published"]

        results.append(scraped_dict)

        time.sleep(0.05)

    return results



final_results = []


for i in range(101,200):

    url = main_url + str(i)
    print(i)
    
    try:
        links = ScrapeUrl(url)
        new_results = ScrapeFrontPage(links)
        final_results += new_results
        
    except Exception as e:
        print("ERROR: {}".format(url))
        print(str(e))
        
    

df = pd.DataFrame(final_results)

print(df.info())
print(df.head())


df.to_csv('/home/daniel/Desktop/Scripts/JupyterNotebooks/WineMag101_200.csv')

duration = time.time() - startTime
minutes = duration // 60
seconds = round(duration % 60)

print("{} min {} sec".format(minutes, seconds))




#print(links)

##
##url = "https://sporza.be/nl/categorie/voetbal/"
##
##class Sporza( scrapy.Spider ):
##
##    name = 'sporza'
##
##    def start_requests( self ):
##        
##        urls = [ "https://beerconnoisseur.com/search-beer"]
##        
##        for url in urls:
##            yield scrapy.Request( url = url, callback = self.parse )
##
##    def parse( self, response ):
##
##        # get all reviews from page
##        rankings = response.xpath('//a/@href')
##        #
##        print(rankings)
##        
##
##
##
##process = CrawlerProcess()
##process.crawl(Sporza)
##process.start()










