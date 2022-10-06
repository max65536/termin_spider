from http import cookies
from scrapy.spiders import Spider
from scrapy.utils.response import open_in_browser
from IPython import embed

class ScanSpider(Spider):
    name = "stadttermin"
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        
    }
    cookie_dict = {
        "cookie_accept":1,
        "TVWebSession":"0g9603741eit44bmg9bn72koa6"
    }

        
    # start_urls = ["https://termine.staedteregion-aachen.de/auslaenderamt/suggest?cnc-145=1"]

    def start_requests(self):
        url = "https://termine.staedteregion-aachen.de/auslaenderamt/suggest?cnc-145=1"
        yield Request(url, headers=self.headers, cookies=self.cookie_dict)

    # def get_cookie(self):
    #     https://termine.staedteregion-aachen.de/auslaenderamt/

    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        # open_in_browser(response)
        with open("response.html", "w") as f:
            f.write(response.text)

        titles = response.xpath('//a[@class="post-title-link"]/text()').extract()
        for title in titles:
            print(title.strip())