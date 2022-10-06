from http import cookies
from scrapy.spiders import Spider
from scrapy.utils.response import open_in_browser
from scrapy import Request
from tkinter import messagebox
import datetime
import requests
from IPython import embed

class ScanSpider(Spider):
    name = "stadttermin"
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36",
        
    }
    cookie_dict1 = {
        "cookie_accept":1,
        "TVWebSession":"xxxxxxxxxx"
    }

    cookie_dict2 = {
        "cookie_accept":1,
        "TVWebSession":"xxxxxxxxxx"
    }

        
    # start_urls = ["https://termine.staedteregion-aachen.de/auslaenderamt/suggest?cnc-145=1"]

    def start_requests(self):
        # url = "https://termine.staedteregion-aachen.de/auslaenderamt/suggest?cnc-145=1"
        # yield Request(url, headers=self.headers, cookies=self.cookie_dict)
        url = "https://termine.staedteregion-aachen.de/auslaenderamt/"
        yield Request(url, headers=self.headers)

    # def get_cookie(self):
    #     https://termine.staedteregion-aachen.de/auslaenderamt/

    def parse(self, response):
        # from scrapy.shell import inspect_response
        # inspect_response(response, self)
        # open_in_browser(response)


        # for title in titles:
        #     print(title.strip())
        
        
        self.cookie = response.headers['Set-Cookie']

        next_url = "https://termine.staedteregion-aachen.de/auslaenderamt/select2?md=1"
        # embed()
        self.cookie_dict1["TVWebSession"] = self.cookie.split()[0][13:-1].decode('utf-8')
        yield Request(next_url, headers=self.headers, cookies=self.cookie_dict1, callback=self.parse_step2)

        error = response.xpath('//h1[@class="error"]').extract()
        data = response.xpath('//div[@id="inhalt"]/h1/text()').extract()
        # print("---------------------------data-----------------------------\n", data)
        print(datetime.datetime.now())
        print(data)

    def parse_step2(self,response):
        # with open("response.html", "w") as f:
        #     f.write(response.text)
        self.cookie = response.headers['Set-Cookie']
        self.cookie_dict2["TVWebSession"] = self.cookie.split()[0][13:-1].decode('utf-8')
        next_url = "https://termine.staedteregion-aachen.de/auslaenderamt/suggest?cnc-145=1&loc=16"
        yield Request(next_url, headers=self.headers, cookies=self.cookie_dict2, callback=self.parse_step3)
        data = response.xpath('//div[@id="inhalt"]/h1/text()').extract()
        # print("---------------------------data-----------------------------\n", data)
        print(data)

    def parse_step3(self, response):        
        error = response.xpath('//h1[@class="error"]').extract()
        data = response.xpath('//div[@id="inhalt"]/h1/text()').extract()
        # print("---------------------------data-----------------------------\n", data)
        # print("---------------------------error-----------------------------\n", error)
        print(data, error)
        with open("response.html", "w") as f:
            f.write(response.text)
        if "Keine" in data[0]:
            # messagebox.showinfo("test")
            pass
        else:
            messagebox.showinfo("New Termin!")
        # embed()