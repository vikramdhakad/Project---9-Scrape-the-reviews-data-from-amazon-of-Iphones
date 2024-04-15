import scrapy
from scrapy.crawler import Crawler
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from time import sleep

class ScraperSpider(scrapy.Spider):
    name = "scraper"
    allowed_domains = ["www.amazon.in"]
    start_urls = ["https://www.amazon.in/Apple-iPhone-15-128-GB/product-reviews/B0CHX1W1XY/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews"]
 
    headers = {
        "Accept-Ch": "ect,rtt,downlink,device-memory,sec-ch-device-memory,viewport-width,sec-ch-viewport-width,dpr,sec-ch-dpr,sec-ch-ua-platform,sec-ch-ua-platform-version",
        "Accept-Ch-Lifetime": "86400",
        "Alt-Svc": "h3=':443'; ma=86400",
        "Cache-Control": "no-cache",
        "Cache-Control": "no-transform",
        "Content-Encoding": "gzip",
        "Content-Language": "en-IN",
        "Content-Security-Policy": "upgrade-insecure-requests;report-uri https://metrics.media-amazon.com/",
        "Content-Security-Policy-Report-Only": "default-src 'self' blob: https: data: mediastream: 'unsafe-eval' 'unsafe-inline';report-uri https://metrics.media-amazon.com/",
        "Content-Type": "text/html;charset=UTF-8",
        "Date": "Mon, 08 Apr 2024 05:11:02 GMT",
        "Expires": "-1",
        "Pragma": "no-cache",
        "Server": "Server",
        "Set-Cookie": "session-token=vpRRkU2lkNUQuaAdaBcd/uwIgAIO/CpvhdXQ3iCOiDP7qD1KJapOWMHt7DRpBRv+Yu17a048VHOvgamaTS4zY/jOSRPrlYnRb/mB1LIX1n1v327Bys7UBDVnpKiX4ZmiN3WRlGbtuZKMFZEIywgz15EZnIhJ55HZDYrs+lFrx5/acn/KglqBot0pwUIygQ0CeKIg5/4ceQC0iosxZCJMyoHEq7kC9QuD73cZD1wXMdkxiJYjUn4TX/OapRLaX6T4xFM+bDNEWXnG14KGJ6ThXM8UPcnjU7Lw3PL4R8gDBPLSizhbQji9rGvZi6jUn/txKF9XKc5tUgsmpCaZO03ZTGL1IWOXHXJf; Domain=.amazon.in; Expires=Tue, 08-Apr-2025 05:11:02 GMT; Path=/; Secure",
        "Strict-Transport-Security": "max-age=47474747; includeSubDomains; preload",
        "Vary": "Content-Type,Accept-Encoding,User-Agent",
        "Via": "1.1 26fdfa679450342b5a2c6d7b18a66f50.cloudfront.net (CloudFront)",
        "X-Amz-Cf-Id": "U2BtvbIOdsSL92RavptiLOek6j2PXhUHrJtRLWPCBG0pcMhB8YoD4A==",
        "X-Amz-Cf-Pop": "BOM54-P1",
        "X-Amz-Rid": "C7BRMGN50G4CPTNKY41X",
        "X-Cache": "Miss from cloudfront",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "SAMEORIGIN",
        "X-Xss-Protection": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 OPR/107.0.0.0"
    }
    
    rules = (Rule(LinkExtractor(allow="")),)

    custom_settings = {
        'DEFAULT_REQUEST_HEADERS': headers
    }

    def parse(self, response):
        
        for box in response.xpath("//*[@class='a-section celwidget']"):
            user_name = box.xpath("div[1]/a/div[2]/span/text()").get()
            review_title = box.xpath("div[2]/a/span[2]/text()").get()
            rating = box.xpath("div[2]/a/i/span/text()").get()
            review = box.xpath("div[4]/span/span/text()").get()
            
            # yield{
            #     "User_Name": user_name,
            #     "Review_Title": review_title,
            #     "Rating": rating,
            #     "Review": review
            # }
        
        # next_page = response.xpath("//*[@id='cm_cr-pagination_bar']/ul/li[2]/a").get()
        # if next_page:
        #     yield response.follow(url=next_page, callback=self.parse)
        
        for page in response.xpath("//*[@id='cm_cr-pagination_bar']/ul/li[2]/a"):
            nxt = page.xpath("@href").get()
            next_page = response.urljoin(nxt)
            yield response.follow(url=next_page,callback=self.parse)
            
            for box in response.xpath("//*[@class='a-section celwidget']"):
                user_name = box.xpath("div[1]/a/div[2]/span/text()").get()
                review_title = box.xpath("div[2]/a/span[2]/text()").get()
                rating = box.xpath("div[2]/a/i/span/text()").get()
                review = box.xpath("div[4]/span/span/text()").get()
            
                yield{
                    "User_Name": user_name,
                    "Review_Title": review_title,
                    "Rating": rating,
                    "Review": review
                }
