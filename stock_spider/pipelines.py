# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from scrapy.exporters import CsvItemExporter
from stock_spider.items import *
import os
import re
import json

CATEGORY = 'category'
DIRECTORY = 'data/aastocksIndustry/'
class StockSpiderPipeline:
    def open_spider(self, spider):
        crawlALL = spider.crawlAll
        filename = f'{DIRECTORY}config.json'
        if os.path.exists(filename):
            with open(filename, 'r') as f:
                config = json.load(f)
                itemList = config['itemList']

        self.items = {}        
        for key in itemList.keys():
            if not crawlALL and 'Tab' in key:
                continue
            value = itemList[key]
            s = re.search('(.+)Item', key).group(1)
            filename = f'{DIRECTORY}{s}.csv'
            file = open(filename, 'wb') 
            exporter = CsvItemExporter(file , encoding='utf-8-sig')
            exporter.fields_to_export = value
            exporter.start_exporting()
            self.items[key] = (exporter, file)

    def close_spider(self, spider):
        for exporter, file in self.items.values():
            exporter.finish_exporting()
            file.close()

    def process_item(self, item, spider):
        key = type(item).__name__
        exporter = self.items[key][0]
        exporter.export_item(item)
        return item
        
