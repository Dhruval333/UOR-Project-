import scrapy


# item class included here 
class WorkItem(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    attr = scrapy.Field()


class WorkSpider(scrapy.Spider):
    name = "WorkScript"

    start_urls = [
    "https://www.uregina.ca/external/communications/feature-stories/current/2019/index.html"
    ]

    BASE_URL = 'https://www.uregina.ca/external/communications/feature-stories/current/2019/index.html'

    def parse(self, response):
        links = response.xpath('//td[@class="title"]/a/@href').extract()
        for link in links:
            absolute_url = self.BASE_URL + link
            yield scrapy.Request(absolute_url, callback=self.parse_attr)

    def parse_attr(self, response):
        item = WorkItem()
        item["link"] = response.url
        item["author"] = response.css('span::text')[2].get()  #author
        item["text"] = response.css('div.cutline::text').get()  #description
        item["date"] = response.css('span::text')[4].get() #date
        item["img"] = response.css('div.primaryImage img').attrib['src']
        # item["attr"] = "".join(response.xpath("//p[@class='attrgroup']//text()").extract())
        return itemimport scrapy

# single link
link=response.css('td.title a:nth-child(1)::attr(href)').get()
# all links
link=response.css('td.title a:nth-child(1)::attr(href)').extractget()
# response.xpath('//*[@id="dspace"]/div/div/p[1]/span[1]/text()').getall()  
# response.css('td.title a::attr(href)').getall()
 

     