# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from settings import IMAGES_STORE
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import csv


class VipGoodPipeline(object):
    def __init__(self):
        self.num = 1
        # 第三种：写入csv文档
        self.f = file(str(self.num)+'.csv','w')
        # 创建csv读写对象
        self.csvwriter = csv.writer(self.f)
        csvhead = ['type_path', 'type_name', 'good_price', 'brand_id', 'good_name', 'img_name', 'good_link', 'img_url']
        self.csvwriter.writerow(csvhead)
        # 第二种：写入json文档
        # self.f = open(str(self.num)+'.json',"w")
        # 第一种：写入txt文档
        # self.f = open(str(self.num) + '.txt', "w+")

    def process_item(self, item, spider):
        # 第三种
        data = item.values()
        self.csvwriter.writerow(data)
        # 第二种
        # content = json.dumps(dict(item), ensure_ascii=False)+',\n'
        # self.f.write(content)
        # 第一种
        # self.f.write(str(item))
        return item

    def spider_closed(self,spider):
        self.f.close()
        self.num += 1


class ImagesPipeline(ImagesPipeline):
    # settings中设置的图片存储绝对路径命名固定
    img_basepath = IMAGES_STORE

    def get_media_requests(self, item, info):
        img_url = item['img_url']
        yield scrapy.Request(img_url)

    def item_completed(self, results, item, info):
        image_path = [x["path"] for ok, x in results if ok]
        os.rename(self.img_basepath + "/" + image_path[0], self.img_basepath + item['type_path'][1:]+'/'+item['img_name']+'.jpg')
        item['img_path'] = self.img_basepath + item['type_path']+item['img_name']+'.jpg'

        return item
