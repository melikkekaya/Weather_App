import scrapy

class HollandSpider(scrapy.Spider):
    name = "Holland"
    #allowed_domains = ["tr.wikipedia.org"]
    start_urls = ["https://tr.wikipedia.org/wiki/Hollanda%27daki_%C5%9Fehirler_listesi"]

    def parse(self, response):

        for i in response.css(".wikitable sortable jquery-tablesorter"):
            city_name = i.css("a.href::text()").get()
            state_name = i.css("a.href::text()").get()
            #population = i.css("td[5]").get()

        yield{
                "States " : state_name,
                "City " : city_name
                #"Population" : population
            }    



        # results = response.xpath('//*[@id="mw-content-text"]/div[1]/table/text()').get()
        # for i in results:
        #     city_name = results.xpath('.//*[@id="mw-content-text"]/div[1]/table/tbody/tr[1]/td[2]/a/text()')
        #     state_name = results.xpath('.//*[@id="mw-content-text"]/div[1]/table/tbody/tr[1]/td[7]/a/text()').get()
        #     population = results.xpath('.//*[@id="mw-content-text"]/div[1]/table/tbody/tr[1]/td[6]').get() 

        #     yield{
        #         "City" : city_name,
        #         "State": state_name,
        #         "Population": population
                
        #         }        
    
