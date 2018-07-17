import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/tag/humor/',
    ]
    
    def parse(self, response):
        for quote in response.css('div.quote'):
            #link = quote.xpath('span/a/@href').extract_first()
            yield scrapy.Request(response.urljoin(link), callback=self.parse_attr)
        next_page = response.css('li.next a::attr("href")').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
            
   def parse_attr(self, response):
        item = {}
        item["text"] = response.css('span.text::text').extract_first()
        item["author"] = response.xpath('span/small/text()').extract_first()
        item["tag"] = response.css('a.tag::text').extract()
        item["born"] = response.css('span.author-born-location::text').extract_first()
        yield item
