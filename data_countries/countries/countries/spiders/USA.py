import scrapy


class UsaSpider(scrapy.Spider):
    name = "usa_data"
    start_urls = ["https://en.wikipedia.org/wiki/List_of_United_States_cities_by_population"]

    def parse(self, response):
        for row in response.css("table.wikitable.sortable tr")[:-48]:
            city_name = row.css("td:nth-child(2) a::text").get()
            state_name = row.css("td:nth-child(3) a::text").get()
            population = row.css("td:nth-child(4)::text").get()
            if city_name is not None and state_name is not None and population is not None:
                yield {
                    "city_name": city_name.strip(),
                    "state_name": state_name.strip(),
                    "population": population.strip()
                }