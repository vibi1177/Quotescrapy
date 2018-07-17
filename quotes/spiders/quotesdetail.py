# -*- coding: utf-8 -*-
import scrapy


class QuotesSpiderDetail(scrapy.Spider):
    name = "quotesdetail"
    start_urls = [
        'http://quotes.toscrape.com/tag/humor/',
    ]
    
    def parse(self, response):
        for quote in response.css('div.quote'):
            link = quote.xpath('span/a/@href').extract_first()
            yield scrapy.Request(response.urljoin(link), callback=self.parse_attr_quote)
        next_page = response.css("li.next a::attr(href)").extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
            
            
    def parse_attr_quote(self, response):
        item = {}
        item["text"] = response.css("h3.author-title::text").extract_first()
        item["description"] = response.css("p.author-description::text").extract_first()
        item["born"] = response.css("span.author-born-location::text").extract_first()
        yield item
