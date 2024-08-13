import scrapy

from scrapy.loader import ItemLoader
from itemloaders.processors import MapCompose
from ..items import IllustrationsDownloaderItem


class IllustrationsSpider(scrapy.Spider):
    name = "illustrations"
    allowed_domains = ["unsplash.com"]
    start_urls = ["https://unsplash.com"]

    def parse(self, response):
        for image_page in response.xpath('//*[@itemprop="contentUrl"]/@href').extract():
            yield scrapy.Request(response.urljoin(image_page), self.parse_image_page)

    def parse_image_page(self, response):
        loader = ItemLoader(item=IllustrationsDownloaderItem(), response=response)
        loader.default_input_processor = MapCompose(str.strip)
        loader.add_xpath('name', '//h1/text()')
        loader.add_xpath('published', '//time/text()')
        full_image_url = response.xpath('//*[@class="wdUrX"]/img[2]/@src').extract_first()
        loader.add_value('image_urls', full_image_url)

        yield loader.load_item()
