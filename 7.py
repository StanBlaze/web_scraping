import scrapy

class QuotesSpider(scrapy.Spider):
    name = "quotestoscrape"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]
    max_count_follow = 1  

    custom_settings = {
        'DOWNLOAD_DELAY': 1  
    }

    def parse(self, response):
        quotes = response.xpath('//div[@class="quote"]')
        for quote in quotes:
            text = quote.xpath('span[@class="text"]/text()').get()
            author = quote.xpath('span/small[@class="author"]/text()').get()

            yield {
                'text': text,
                'author': author
            }

 
        next_btn = response.xpath('//li[@class="next"]/a/@href').get()
        if next_btn and self.max_count_follow > 0:
            self.max_count_follow -= 1
            yield response.follow(next_btn, callback=self.parse)
