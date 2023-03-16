import scrapy
from ..items import BookscraperItem

class BooksSpider(scrapy.Spider):
    name = "books"
    page=2
    start_urls = [
            "https://www.amazon.in/s?i=stripbooks&bbn=976389031&rh=n%3A976389031%2Cp_n_publication_date%3A2684819031&dc&page=1&qid=1678925799&rnid=2684818031&ref=sr_pg_2"
            ]

    def parse(self, response):
        items = BookscraperItem()

        name = response.css('.a-color-base.a-text-normal').css('::text').extract()
        author = response.css('.a-row .a-color-secondary:nth-child(1)').css('::text').extract()
        price = response.css('.a-price-whole').css('::text').extract()
        cover = response.css('.s-image::attr(src)').extract()

        items['name'] = name
        items['author'] = author
        items['price'] = price
        items['cover'] = cover
    
        yield items

        next_page = f"https://www.amazon.in/s?i=stripbooks&bbn=976389031&rh=n%3A976389031%2Cp_n_publication_date%3A2684819031&dc&page={str(self.page)}&rnid=2684818031&ref=sr_pg_{str(self.page)}"
        if self.page<11:
            self.page+=1
            yield response.follow(next_page, callback=self.parse)
