import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/tag/humor/',
    ]
    
    def parse(self, response):
        for quote in response.css('div.quote'):
            yield  scrapy.Request(quote, callback=self.parse_attr),
        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
            
   def parse_attr(self, response):
        item = QuotesItem()
        links = response.xpath('span/a/@href').extract()
        BASE_URL = 'http://quotes.toscrape.com/'
        for link in links:
            absolute_url = self.BASE_URL + link
            item["text"] = response.css('span.text::text').extract_first(),
            item["author"] = response.xpath('span/small/text()').extract_first(),
            item["tag"] = response.css('a.tag::text').extract(),
            item["born"] = response.css('span.author-born-location::text').extract_first()
        yield item
