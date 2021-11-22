import scrapy
from scrapy import FormRequest


class QuotesLoginSpider(scrapy.Spider):
    name = 'quotes_login'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['https://quotes.toscrape.com/login']

    def parse(self, response):
        csrf_token = response.xpath('//input[@name="csrf_token"]/@value').get()
        yield FormRequest.from_response(
            response,
            formxpath='//form',
            formdata={
                'csrf_token': csrf_token,
                'username': 'admin',
                'password': 'admin'
            },
            callback=self.after_login
        )

    def after_login(self, response):
        if response.xpath("//a[@href='/logout']/text()").get():
            print('logged in')

# class OpenlibraryLoginSpider(scrapy.Spider):
#     name = 'openlibrary_login'
#     allowed_domains = ['openlibrary.org']
#     start_urls = ['https://openlibrary.org/account/login']

#     def parse(self, response):
#         yield FormRequest.from_response(
#             response,
#             formid='register',
#             formdata={
#                 'username': 'meinherz75@gmail.com',
#                 'password': 'test123',
#                 'redirect': '/',
#                 'debug_token': '',
#                 'login': 'Log In'
#             },
#             callback=self.after_login
#         )
    
#     def after_login(self, response):
#         print('logged in...')
