# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
#
# Crawl Amazon.com for skincare products

import scrapy


class SkincareSpider(scrapy.Spider):
    name = "skincare"
    start_urls = urls = [
            'https://www.amazon.com/s?rh=n%3A3760911%2Cn%3A%2111055981%2Cn%3A11060451%2Cn%3A11060711&s=review-rank&qid=1562212393&ref=lp_11060711_st'
        ]

    def parse(self, response):
        product_link_list = response.css('.s-line-clamp-4 a::attr(href)').getall()
        for product_link in product_link_list:
            if product_link is not None:
##                yield {
##                 "product_link" : product_link
                yield response.follow(product_link, callback=self.parseProductPage)
##             }
               
        
    def parseProductPage(self, response):
        ingred_list = response.css('.content:nth-child(3) p::text').get()
        
        self.log("Ingredient List: %s" % ingred_list)
        if ingred_list is not None:
            yield
            {
                'ingredient_list' : ingred_list
            }
        else:
            yield
            {
                'response' : None
            }
