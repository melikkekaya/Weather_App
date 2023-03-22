import scrapy

class GermanySpider(scrapy.Spider):
    name = "germany_data"

    #allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_cities_in_Germany_by_population"]
    
    def parse(self, response):

        for row in response.css("table.wikitable.sortable tr"):
            city_name = row.css("td:nth-child(2) a::text").get()
            state_name = row.xpath('.//td[3]/a/text()').get()
            population = row.css('td:nth-child(4)::text').get()
            if city_name is not None:
                yield {
                    "city_name": city_name.strip(),
                    "state_name": state_name.strip(),
                    "population": population.strip()
                }
