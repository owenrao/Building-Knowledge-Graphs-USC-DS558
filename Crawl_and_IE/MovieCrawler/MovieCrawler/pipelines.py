# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from fileinput import filename
from itemadapter import ItemAdapter
import json
from scrapy.exceptions import DropItem

class MoviePipeline:
    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        try: id = adapter['title']+"_"+item.__class__.__name__
        except KeyError: id = adapter['name']+"_"+item.__class__.__name__
        if id in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(id)
            file_name = item.file_name()
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            with open(file_name, 'a') as file:
                file.write(line)
            print("File Written: "+file_name)
            return item


class JsonWriterPipeline:

    def open_spider(self, spider):
        self.file = open('items.jl', 'w')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
        

class DuplicatesPipeline:

    def __init__(self):
        self.ids_seen = set()

    def process_item(self, item):
        adapter = ItemAdapter(item)
        if adapter['id'] in self.ids_seen:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            self.ids_seen.add(adapter['id'])
            return item
