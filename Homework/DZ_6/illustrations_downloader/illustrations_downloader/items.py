# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IllustrationsDownloaderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    published = scrapy.Field() # хранения даты или времени публикации изображения
    image_urls = scrapy.Field() # хранение списка URL-адресов изображений
    images = scrapy.Field() # информация о загруженных изображениях

