import scrapy


class BelgiumSpider(scrapy.Spider):
    name = "Belgium"
    #allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_most_populous_municipalities_in_Belgium"]

    def parse(self, response):

        for i in response.css(".wikitable sortable jquery-tablesorter"):
            city_name = i.css("href::text").get()
            state_name = i.css("").get()
            population = i.css("").get()
            


        yield{
                "City" : city_name,
                "State": state_name,
                "Population": population
                }      
       

# for i in response.css(".work-process-card"):
#             weeks = i.css("span.number::text").get().strip()
#             headings = i.css('h3::text').get()
#             desc = i.css('p::text').get()