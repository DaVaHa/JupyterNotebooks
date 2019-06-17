import scrapy
from scrapy.crawler import CrawlerProcess
import time


class WineMagSpider( scrapy.Spider ):

    name = 'wine_mag_spider'

    # start
    def start_requests( self ):

        main_url = "https://www.winemag.com/?s=&drink_type=wine&page="
        urls = [main_url+str(i) for i in range(1,100)]

        for url in urls:
            time.sleep(1)
            yield scrapy.Request( url = url, callback = self.parse)


    # parse front page
    def parse( self, response ):

        time.sleep(1)
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

        file = 'winemag_v1_1000.csv'
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


        file = 'winemag_extra_v1_1000.csv'
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
<ul class="secondary-info">
                                                    <li class="row">
                    <div class="info-label small-7 columns">
                      <span>Alcohol</span>
                    </div>
                    <div class="info small-9 columns">
                      <span><span>13%</span></span>
                    </div>
                  </li>
                                                    <li class="row">
                    <div class="info-label small-7 columns">
                      <span>Bottle Size</span>
                    </div>
                    <div class="info small-9 columns">
                      <span><span>750 ml</span></span>
                    </div>
                  </li>
                                                    <li class="row">
                    <div class="info-label small-7 columns">
                      <span>Category</span>
                    </div>
                    <div class="info small-9 columns">
                      <span><span>White</span></span>
                    </div>
                  </li>
                                                    <li class="row">
                    <div class="info-label small-7 columns">
                      <span>Importer</span>
                    </div>
                    <div class="info small-9 columns">
                      <span><span>Luiz's Grocery and Liquors</span></span>
                    </div>
                  </li>
                                                    <li class="row">
                    <div class="info-label small-7 columns">
                      <span>Date Published</span>
                    </div>
                    <div class="info small-9 columns">
                      <span><span>5/1/2019</span></span>
                    </div>
                  </li>
                                                    <li class="row">
                    <div class="info-label small-7 columns">
                      <span>User Avg Rating</span>
                    </div>
                    <div class="info small-9 columns">
                      <span><span><span id="user-rating">Not rated yet</span> <a href="" id="show_add-review">[Add Your Review]</a></span></span>
                    </div>
                  </li>
                              </ul>
"""

