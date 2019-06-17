import scrapy
from scrapy.crawler import CrawlerProcess
import time
import numpy as np

# URL
url = "http://www.winemag.com/?s=&drink_type=wine&page=1"

results = []


def GenerateIPAdress():
    i = np.random.randint(11,99)
    j = np.random.randint(0,99)
    k = np.random.randint(101,200)
    l = np.random.randint(201,300)
    ip = str(i) + '.' + str(j) + '.' + str(k) + '.' + str(l)
    print("IP : " + ip)
    return ip

class WineMagSpider( scrapy.Spider ):

    name = 'wine_mag_spider'

    # start
    def start_requests( self ):

        #main_url = "https://www.winemag.com/?s=&drink_type=wine&page="
        main_url = "https://www.winemag.com/?s=&drink_type=wine&pub_date_web=2017&page="
        urls = [main_url+str(i) for i in range(1,1150)]

        for url in urls:

            if urls.index(url) % 8 == 0:
                ip = GenerateIPAdress()

            #time.sleep(1)
            yield scrapy.Request( url = url, callback = self.parse ,
            headers= {  'user-agent': ('Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 '
                       '(KHTML, like Gecko) Chrome/{0} Safari/537.36'.format(ip))
                     }
                       )

    # parse front page
    def parse( self, response ):

        time.sleep(2)
        # get all items from page
        items = response.xpath('//li[contains(@class,"review-item")]')

        title = items.xpath('.//div[contains(@class,"title")]/text()').extract()
        rating = items.xpath('.//div[contains(@class,"info")]/span[contains(@class,"rating")]//text()').extract()
        price = items.xpath('.//span[contains(@class,"price")]/text()').extract()
        appellation = items.xpath('.//span[contains(@class,"appellation")]/text()').extract()
        hrefs = items.xpath('./a[contains(@class,"review-listing")]/@href').extract()

        rating = [r for r in rating if 'POINTS' not in r.upper()]

        #print(len(title))
        #print(len(rating))
        #print(len(price))
        #print(len(appellation))
        #print(len(hrefs))

        #file = 'winemag_v3000_4000.csv'
        file = 'winemag_v2017.csv'

        with open(file, 'a') as f:
            for i in range(len(title)):
                f.writelines( [hrefs[i] + '|' + title[i] + '|' + rating[i] + '|' + price[i] + '|' + appellation[i] + '\n'])

        for href in hrefs:
            yield response.follow(url = href, callback = self.parse_extra_info)
            #pass

    # parse link
    def parse_extra_info(self, response):

        time.sleep(1)
        #print(response.url)
        url = response.url

        extra = response.xpath('//ul[@class="secondary-info"]')

        labels = extra.xpath('.//div[@class="info-label small-7 columns"]//text()')
        values = extra.xpath('.//div[@class="info small-9 columns"]//text()')

        data = dict(zip([l.extract().strip() for l in labels],[v.extract().strip() for v in values]))

        #print(data)


        alcohol, category, date = None, None, None

        if "Alcohol" in data.keys(): alcohol = data["Alcohol"]
        if "Category" in data.keys(): category = data["Category"]
        if "Date Published" in data.keys(): date = data["Date Published"]


        #file = 'winemag_extra_v3000_4000.csv'
        file = 'winemag_extra_v2017.csv'
        with open(file, 'a') as f:
            f.writelines( [url + '|' + alcohol + '|' + category + '|' + date + '\n'])



process = CrawlerProcess()
process.crawl(WineMagSpider)
process.start()

"""
                     <li class="review-item ">
              <div class="review-ranking">0</div> <a class="review-listing" href="https://www.winemag.com/buying-guide/chateau-haut-brion-2016-pessac-leognan-310320/" data-review-id="310320">
        <div class="title">Château Haut-Brion 2016  Pessac-Léognan</div>
        <div class="excerpt">Immensely tannic, this is a great Haut-Brion, one of the finest for&nbsp;...</div>
        <div class="info">
          <span class="rating"><strong>100</strong> Points</span>
          <span class="appellation">Bordeaux</span>
          <span class="price">$650</span>
          <br /><span class="badge">Cellar Selection</span>
        </div>
      </a>          </li>
"""
"""
        #title = link.find('div', class_="title").text
        #rating = link.find('span', class_="rating").text
        #price = link.find('span', class_="price").text
        #excerpt = link.find('div', class_="excerpt").text
        #appellation = link.find('span', class_="appellation").text
        #badge = link.find('span', class_="badge").text
        #print(title, rating, price, appellation)
        #href = link.find('a').get('href')


"""
"""
  # start_requests method
  def start_requests(self):
    yield scrapy.Request(url = url_short,
                         callback = self.parse_front)
  # First parsing method
  def parse_front(self, response):
    course_blocks = response.css('div.course-block')
    course_links = course_blocks.xpath('./a/@href')
    links_to_follow = course_links.extract()
    for url in links_to_follow:
      yield response.follow(url = url,
                            callback = self.parse_pages)
  # Second parsing method
  def parse_pages(self, response):
    crs_title = response.xpath('//h1[contains(@class,"title")]/text()')
    crs_title_ext = crs_title.extract_first().strip()
    ch_titles = response.css('h4.chapter__title::text')
    ch_titles_ext = [t.strip() for t in ch_titles.extract()]
    dc_dict[ crs_title_ext ] = ch_titles_ext
"""
