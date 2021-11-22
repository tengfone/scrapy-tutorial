# 4D-Scraping

## Setup

From https://www.udemy.com/course/web-scraping-in-python-using-scrapy-and-splash/

```py
pip install scrapy
```

```py
scrapy shell
fetch("URL")
response
response.css('div.xxxx').get() # First item on list
products = response.css('div.product-item-info')
products.css('a.product-item-link::text').get() / .getall()
products.css('a.product-item-link').attrib['href']
```

If there are spaces in classes, replace it with dot. Eg "a.action next" == "a.action.next"

```bash
cd to ./scrapyTutorial
scrapy crawl xxxx -o output.json
```

For pagination refer to special_offers.  
For normal request refer to countryspider.  
For uncoding json/change header, refer to settings.py  
For multiple change header, change default_request_headers OR change in start_request in spider  
For debugging, can use scrapy parse --spider=spidername -c FUNCTION_NAME --meta='{\"country_name\":"\China\"}' https://smthsmth OR we can use from scrapy.shell import inspect_response. Then just use inspect_response(response, self) OR just use logging OR BEST, use runner.py

Crawler

```
scrapy genspider -t crawl FILE_NAME WEBSITE.COM
```

Look at rules and request headers.

For lazy loading / Javascript. Need use Splash.

```
docker pull scrapinghub/splash
docker run -it -p 8050:8050 scrapinghub/splash
```

For duckduckgo on splash:

```lua
function main(splash, args)
  --splash:set_user_agent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36")
  --headers = {
    --['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'
  --}
  --CALLBACK
  splash:on_request(function(request)
  	request:set_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36')
  end)
  splash:set_custom_headers(headers)
  assert(splash:go(args.url))
  assert(splash:wait(0.5))
  input_box = assert(splash:select("#search_form_input_homepage"))
  input_box:focus()
  input_box:send_text("my user agent")
  assert(splash:wait(0.5))
  --[[
  btn = assert(splash:select("#search_button_homepage"))
  btn:mouse_click()
  --]]

  input_box:send_keys("<Enter>")
  assert(splash:wait(3))
  splash:set_viewport_full()
  return {
    html = splash:html(),
    png = splash:png(),
  }
end

-- https://web.archive.org/web/20200116052415/https://www.livecoin.net/en/
function main(splash, args)
  splash.private_mode_enabled=false
  url = args.url
  assert(splash:go(url))
  assert(splash:wait(3))
  rur_tab = assert(splash:select_all(".filterPanelItem___2z5Gb"))
  rur_tab[5]:mouse_click()
  assert(splash:wait(1))
  splash:set_viewport_full()
  return splash:png()
end
```

To use scrapy with splash, pip install scrapy-splash. To use scrapy with selenium use middleware (scrapy-selenium).

Pipelining (Send result to database)
in pipelines.py. (IMDB) and settings.py need to uncomment the item_pipelines.

CLASS METHODS: https://www.youtube.com/watch?v=PNpt7cFjGsM

To store on mongoDB, use pip install pymongo dnspython.

API Scraping - demo_api
LOGIN - demo_login (if need jaavascript, use scrapy_splash import splashform request)

```py
import scrapy
from scrapy_splash import SplashRequest, SplashFormRequest


class QuotesLoginSpider(scrapy.Spider):
    name = 'quotes_login'
    allowed_domains = ['quotes.toscrape.com']

    script = '''
        function main(splash, args)
          assert(splash:go(args.url))
          assert(splash:wait(0.5))
          return splash:html()
        end
    '''

    def start_requests(self):
        yield SplashRequest(
            url='https://quotes.toscrape.com/login',
            endpoint='execute',
            args = {
                'lua_source': self.script
            },
            callback=self.parse
        )

    def parse(self, response):
        csrf_token = response.xpath('//input[@name="csrf_token"]/@value').get()
        yield SplashFormRequest.from_response(
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
```

Cloudflare bypass: https://checkforcloudflare.selesti.com/
look at coinmarketcap - https://github.com/clemfromspace/scrapy-cloudflare-middleware
```py
# ALSO in the spider file, need to go into the middleware class below and change status accordingly
from scrapy_cloudflare_middleware.middlewares import CloudflareMiddleware

# Under settings.py
DOWNLOADER_MIDDLEWARES = {
    # The priority of 560 is important, because we want this middleware to kick in just before the scrapy built-in `RetryMiddleware`.
    'scrapy_cloudflare_middleware.middlewares.CloudFlareMiddleware': 560
}
DUPEFILTER_CLASS = 'scrapy_cloudflare_middleware.filters.CloudflareDupeFilter'
```