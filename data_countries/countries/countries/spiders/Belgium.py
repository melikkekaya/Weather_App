import scrapy

class BelgiumSpider(scrapy.Spider):
    name = "belgium_data"
    
    #allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_most_populous_municipalities_in_Belgium"]
    def parse(self, response):
        for i in response.xpath("//table[@class='wikitable sortable']/tbody/tr[position() > 2]"):
            city_name = i.xpath(".//td[2]/a/text()").get()
            state_name = i.xpath(".//td[9]/a/text()").get()
            population = i.xpath(".//td[7]/text()").get()
            yield{
                "city_name" : city_name,
                "state_name": state_name,
                "population": population
                 }