import scrapy
from pymongo import *
import certifi

class BelgiumSpider(scrapy.Spider):
    name = "belgium_data"
    
    #allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_most_populous_municipalities_in_Belgium"]
    def parse(self, response):
        connection = "mongodb+srv://melike:1234@weatherapp.xzog7un.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(connection, tlsCAFile=certifi.where())
        db = client.get_database ('WeatherApp')
        dbdata = db.test
        for i in response.xpath("//table[@class='wikitable sortable']/tbody/tr[position() > 2]"):
            city_name = i.xpath(".//td[2]/a/text()").get()
            state_name = i.xpath(".//td[9]/a/text()").get()
            population = i.xpath(".//td[7]/text()").get()


            dbdata.insert_one ({
                "country_name": "BE",
                "city_name" : city_name,
                "state_name": state_name,
                "population": population
                 })

            