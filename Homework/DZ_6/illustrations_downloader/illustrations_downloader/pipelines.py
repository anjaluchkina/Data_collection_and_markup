# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import hashlib
from scrapy.pipelines.images import IllustrationsDownloaderPipeline

'''class IllustrationsDownloaderPipeline:
    def process_item(self, item, spider):
        return item'''

class UnsplashImagePipeline(IllustrationsDownloaderPipeline):
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        return super().process_item(item, spider)

    def file_path(self, request, response=None, info=None, *, item=None):
        image_guid = hashlib.sha1(request.url.encode()).hexdigest()
        name = item.get('name', ['image'])[0]
        return f"{name.replace(' ','_')}-{image_guid}.jpg"
