import scrapy
import json
from scrapy.exceptions import CloseSpider


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/api/quotes?page=1']

    def parse(self, response):

        if response.status == 500:
            raise CloseSpider("REACHED LAST")

        print(response.body)
        resp = json.loads(response.body)
        quotes = resp.get('quotes')
        for quote in quotes:
            yield {
                'author': quote.get('author').get('name'),
                'text': quote.get('text'),
                'tags': quote.get('tags')
            }

        has_next = resp.get('has_next')
        if has_next:
            next_page_number = resp.get('page') + 1
            yield scrapy.Request(url=f'https://quotes.toscrape.com/api/quotes?page={next_page_number}', callback=self.parse)
