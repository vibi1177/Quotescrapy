import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/tag/humor/',
    ]

    BASE_URL = 'http://quotes.toscrape.com/'
    
    def parse(self, response):
        for quote in response.css('div.quote'):
            links = quote.xpath('span/a/@href').extract()
            for link in links:
                absolute_url = self.BASE_URL + link
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.xpath('span/small/text()').extract_first(),
                'tag': quote.css('a.tag::text').extract(),
                'detail' : scrapy.Request(absolute_url, callback=self.parse_attr)
            }
            
        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
   def parse_attr(self, response):
        item = QuotesItem()
        item["born"] = response.css('span.author-born-location::text').extract_first()
        return item
