import scrapy
from pymongo import *
import certifi


class UsaSpider(scrapy.Spider):
    name = "usa_data"
    start_urls = ["https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"]

    def parse(self, response):
        connection = "mongodb+srv://melike:1234@weatherapp.xzog7un.mongodb.net/?retryWrites=true&w=majority"
        client = MongoClient(connection, tlsCAFile=certifi.where())
        db = client.get_database ('WeatherApp')
        dbdata = db.test
        for row in response.css("table.wikitable.sortable tr")[:-48]:
            city_name = row.css("td:nth-child(2) a::text").get()
            state_name = row.css("td:nth-child(3) a::text").get()
            population = row.css("td:nth-child(4)::text").get()
            if city_name is not None and state_name is not None and population is not None:
                dbdata.insert_one ({
                    "country_name": "US",
                    "city_name": city_name.strip(),
                    "state_name": state_name.strip(),
                    "population": population.strip()
                })