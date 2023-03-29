import scrapy
from pymongo import *
import certifi

class GermanySpider(scrapy.Spider):
    name = "germany_data"

    #allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_cities_in_Germany_by_population"]
    
    def parse(self, response):
        connection = "mongodb+srv://melike:1234@weatherapp.xzog7un.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(connection, tlsCAFile=certifi.where())
        db = client.get_database ('WeatherApp')
        dbdata = db.test
        for row in response.css("table.wikitable.sortable tr"):
            city_name = row.css("td:nth-child(2) a::text").get()
            state_name = row.xpath('.//td[3]/a/text()').get()
            population = row.css('td:nth-child(4)::text').get()
            if city_name is not None:
                dbdata.insert_one ({
                    "country_name": "DE",
                    "city_name": city_name.strip(),
                    "state_name": state_name.strip(),
                    "population": population.strip()
                })