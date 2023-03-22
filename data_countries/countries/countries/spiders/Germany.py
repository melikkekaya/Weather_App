import scrapy


class GermanySpider(scrapy.Spider):
    name = "Germany"
    #allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_cities_in_Germany_by_population"]

    def parse(self, response):
        pass



        # results = response.xpath('.//*[@id="mw-content-text"]/div[1]/table').get()

        # for i in results:
        #     city_name = results.xpath('//*[@id="mw-content-text"]/div[1]/table/tbody/tr[1]/td[2]/i/b/a/text()').get()
        #     state_name = results.xpath('//*[@id="mw-content-text"]/div[1]/table/tbody/tr[1]/td[3]/a/text()').get()
        #     population = results.xpath('//*[@id="mw-content-text"]/div[1]/table/tbody/tr[1]/td[5]/text()').get()

        #     yield{
        #         "City" : city_name,
        #         "State": state_name,
        #         "Population": population,
        #         }   
