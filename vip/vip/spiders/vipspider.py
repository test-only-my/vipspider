# -*- coding: utf-8 -*-
import scrapy
from vip.items import *
import re
from lxml import etree
import json
import os
# import sys
# reload(sys)
# sys.setdefaultencoding('utf-8')


class VipspiderSpider(scrapy.Spider):
    name = "vipspider"
    allowed_domains = ["vip.com"]
    baseurl = 'http://category.vip.com/'
    typeurl = 'http://category.vip.com/ajax/getCategory.php?callback=getCategory&tree_id=117'
    start_urls = (
        typeurl,
    )

    def parse(self, response):
        # 获得商品的所有分类,json方式请求到的数据
        type_list = response.text[12:-1]
        type_dict = json.loads(type_list)
        item_list = []
        for type in type_dict['data']:
            item = VipGoodItem()
            # 分类名称和链接
            item['type_id'] = type['cate_id']
            item['type_name'] = type['cate_name']
            item['type_link'] = self.baseurl+type['url']
            # type_id = item['type_link'].split('|')[1]
            type_path = './'+item['type_name']
            if not os.path.exists(type_path):
                os.makedirs(type_path)
            item['type_path'] = type_path
            item_list.append(item)
        for item in item_list:
            yield scrapy.Request(item['type_link'], meta={'type_item':item}, callback=self.good_parse)

    def good_parse(self, response):
        # 获取所有的商品
        pattern1 = re.compile(r'list = .*}]')
        goods = pattern1.findall(response.body)
        good_list = goods[0][7:]
        # 字符串格式的列表
        good_dict = json.loads(good_list)

        # 取售卖价格，在字符串中只取数字
        pattern2 = re.compile(r'\d+')
        # 获取当前商品列表页的url,判断是否含有该类别的id
        good_page_url = response.url
        type_item = response.meta['type_item']
        # 如果有这个类别的id，就将类别名一起传递过去
        if type_item['type_id'] in good_page_url:
            for good in good_dict:
                item = VipGoodItem()
                # item['type_id'] = type_item['type_id']
                item['type_name'] = type_item['type_name']
                item['type_path'] = type_item['type_path']

                item['brand_id'] = good['brand_id']
                item['good_name'] = good['show_title']
                item['good_price'] = pattern2.search(good['sell_price']).group()
                # 获取商品分类id和商品id，拼接url
                item['good_link'] = 'http://www.vip.com/detail-'+str(good['brand_id'])+'-'+str(good['id'])+'.html'

                item['img_name'] = good['name']
                item['img_url'] = 'http://'+good['list_img']
                yield item


