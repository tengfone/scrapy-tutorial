import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from spiders.countryspider import CountrySpider


process = CrawlerProcess(settings=get_project_settings())
process.crawl(CountrySpider)
process.start()