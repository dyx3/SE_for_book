# -*- coding: utf-8 -*-
import scrapy
import re

from ..items import BookItem


class BookSpider(scrapy.Spider):
    name = 'bookSpider'
    allowed_domains = ['douban.com']
    start_urls = ['https://book.douban.com/tag']
    count = 0

    def parse(self, response):
        # 爬取内容的标签
        tags = ['小说', '外国文学', '文学', '经典', '中国文学', '随笔', '日本文学',
                '散文', '村上春树', '诗歌', '童话', '名著', '儿童文学', '古典文学',
                '余华', '王小波', '杂文', '当代文学', '张爱玲', '外国名著', '钱钟书',
                '鲁迅', '诗词', '茨威格', '米兰·昆德拉', '杜拉斯', '港台']
        for tag in tags:
            # 翻页
            for i in range(0, 50):
                next_page = next_page = 'https://book.douban.com/tag/' + tag + '?start=' + str(i * 20) + '&type=T'
                yield scrapy.Request(url=next_page, callback=self.parse_page)

    def parse_page(self, response):
        books = response.xpath('//div[@id="subject_list"]/ul/li/div[@class="pic"]/a')
        for book in books:
            detail_url = book.xpath("@href").get()
            yield scrapy.Request(url=detail_url, callback=self.parse_book)

    def parse_book(self, response):
        item = BookItem()
        self.count = 1 + self.count
        print('count is ', self.count)
        # item['count'] = self.count
        item['url'] = response.url
        # 书名
        try:
            item['name'] = response.xpath('//span[@property="v:itemreviewed"]/text()').extract()[0].strip()
        except:
            item['name'] = '无'
        # print(str(self.count), item['name'])
        # 作者
        try:
            item['author'] = response.xpath('//span[contains(text(), "作者")]/following-sibling::a[1]/text()').extract()[
                0].strip().replace(" ", "").replace("\n", "")
        except:
            item['author'] = '无'
        # 出版社
        try:
            item['publisher'] = response.xpath('//span[contains(text(), "出版社")]/following-sibling::text()').extract()[
                0].strip()
        except:
            item['publisher'] = '无'
        # 页数
        try:
            item['page_num'] = int(
                response.xpath('//span[contains(text(), "页数")]/following-sibling::text()').extract()[0].strip())
        except:
            item['page_num'] = 0
        # 定价
        try:
            price = response.xpath('//span[contains(text(), "定价")]/following-sibling::text()').extract()[0].strip()
            item['price'] = 0.0 if (len(price) == 0) else float(re.findall(r'\d+\.?\d*', price)[0])
        except:
            item['price'] = 0.0
        # 装帧
        try:
            item['binding'] = response.xpath('//span[contains(text(), "装帧")]/following-sibling::text()').extract()[
                0].strip()
        except:
            item['binding'] = '无'
        # 丛书
        try:
            item['series'] = response.xpath('//span[contains(text(), "丛书")]/following-sibling::a/text()').extract()[
                0].strip()
        except:
            item['series'] = '无'
        # ISBN
        try:
            item['isbn'] = response.xpath('//span[contains(text(), "ISBN")]/following-sibling::text()').extract()[
                0].strip()
        except:
            item['isbn'] = '无'
        # 简介
        # 简介不需要展开全部的情况
        try:
            intro = ''.join(response.xpath(
                '//div[@class="related_info"]/div[@class="indent"][1]/div[@class]/div[@class="intro"]/p/text()').extract()).replace(
                " ", "").replace("\n", "").replace("\r", "")
            # 简介需要展开
            if not intro:
                intro = ''.join(response.xpath(
                    '//div[@class="related_info"]/div[@class="indent"][1]/span[@class!="short"]/*/div[@class="intro"]/p/text()').extract()).replace(
                    " ", "").replace("\n", "").replace("\r", "")
            item['intro'] = intro if (intro != '') else '无'
        except:
            item['intro'] = '无'
        # 评分
        try:
            item['score'] = float(
                response.xpath('//div[contains(@class, "rating_self ")]/strong/text()').extract()[0].strip())
        except:
            item['score'] = 0.0
        yield item
