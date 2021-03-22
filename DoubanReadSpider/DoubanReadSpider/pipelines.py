# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import csv
import sys
sys.path.append('..')
import es.es_op as op


class DoubanreadspiderPipeline(object):
    def process_item(self, item, spider):
        return item


class ElasticsearchProcessPipeline(object):

    def __init__(self):
        op.create_index('book', True)
        # csv文件的位置,无需事先创建
        # 记录处理失败的图书信息
        path1 = os.path.dirname(__file__) + '/spiders/err_log.csv'
        # 记录爬取成功的图书的书名作者URL
        path2 = os.path.dirname(__file__) + '/spiders/url_list.csv'
        # 打开(创建)文件
        self.file1 = open(path1, 'w', encoding='utf-8', newline='')
        self.file2 = open(path2, 'w', encoding='utf-8', newline='')

        self.writer1 = csv.writer(self.file1)
        self.writer1.writerow(['书名', '作者', 'URL', '索引', '原因'])
        self.writer2 = csv.writer(self.file2)
        self.writer2.writerow(['书名', '作者', 'URL'])

    def process_item(self, item, spider):
        # 保存到elasticsearch
        res = op.insert('book', dict(item))
        if 'error' in res.keys():
            # 保存失败则记录在err_log.csv
            self.writer1.writerow([item['name'], item['author'], item['url'], 'book', str(res)])
        else:
            # 保存成功则将对应的信息存储值url_list.csv
            self.writer2.writerow([item['name'], item['author'], item['url']])
        return item

    def close_spider(self, spider):
        # 关闭爬虫时顺便将文件保存退出
        self.file1.close()
        self.file2.close()
