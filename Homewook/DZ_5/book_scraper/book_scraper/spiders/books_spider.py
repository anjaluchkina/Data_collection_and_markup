import scrapy


class BooksSpiderSpider(scrapy.Spider):
    name = "books_spider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        rows = response.xpath('//article[contains(@class, "product_pod")]')
        for row in rows:
            title = row.xpath('.//h3/a/@title').get()
            price = row.xpath('.//p[@class="price_color"]/text()').get()
            availability = row.xpath('.//p[@class="instock availability"]/text()').get()
            link = row.xpath('.//a/@href').get()


            yield response.follow(url=response.urljoin(link), callback=self.parse_country,
                                  meta={
                                      'title': title,
                                      'price': price,
                                      'availability': availability
                                  })
            
    def parse_country(self, response):
        title = response.meta['title']
        price = response.meta['price']
        availability = response.meta['availability']
        
        product_description = response.xpath('//meta[@name="description"]/@content').get()

        yield {
            'Название': title,
            'Цена': price,
            'Наличие': availability,
            'Описание': product_description.strip() if product_description else None

        }