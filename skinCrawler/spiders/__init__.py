# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
#
# Crawl Amazon.com for skincare products

import scrapy
import json

class SkincareSpider(scrapy.Spider):
    name = "skincare"
    json_array = list()
    start_urls = urls = [
            'https://www.amazon.com/s?i=beauty&rh=n%3A3760911%2Cn%3A11055981%2Cn%3A11060451%2Cn%3A11060711&s=featured-rank&qid=1562260218&ref=sr_st_featured-rank'
        ]

    def parse(self, response):
 ##       product_link_list = response.css('.s-line-clamp-4 a::attr(href)').getall()
        product_link_list = response.css('.a-link-normal.a-text-normal::attr(href)').getall()
        next_page = response.css('.a-last a::attr(href)').get()
        for product_link in product_link_list:
            if product_link is not None:
                yield response.follow(product_link, callback=self.parseProductPage)
        
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)

        
    def parseProductPage(self, response):
        important_content = response.css('#importantInformation .content').get()
        if important_content is not None:
            startIndex = important_content.find('Ingredients')
            startIndex = important_content.find('>', startIndex) + 1
            endIndex = important_content.find('<', startIndex)
            ingred_list = important_content[startIndex:endIndex]
 ##           self.log("Ingredient List: %s" % ingred_list)
            if ingred_list is not None:
                self.json_array.append(dict(ingredient=ingred_list))
        self.writeToJson()
        
        
    def writeToJson(self):
        f = open('skincare.json', 'wb')
        json.dump(self.json_array, f)
        return 
