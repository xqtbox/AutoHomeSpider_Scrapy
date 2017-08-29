# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyAutohomeItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    # 车ID
    CAR_ID = scrapy.Field()
    # 车名
    CAR_NAME = scrapy.Field()

    # 用户ID
    USER_ID = scrapy.Field()
    # 用户名
    USER_NAME = scrapy.Field()

    # 购买地点
    PURCHASE_PLACE = scrapy.Field()
    # 购买时间
    PURCHASE_TIME = scrapy.Field()
    # 裸车购买价
    CAR_PRICE = scrapy.Field()
    # 购车目的
    PURCHASE_PURPOSE = scrapy.Field()

    # 评分- 空间
    SCORE_SPACE = scrapy.Field()
    # 评分- 动力
    SCORE_POWER = scrapy.Field()
    # 评分- 操控
    SCORE_CONTROL = scrapy.Field()
    # 评分- 油耗
    SCORE_FUEL_CONSUMPTION = scrapy.Field()
    # 评分- 舒适性
    SCORE_COMFORT = scrapy.Field()
    # 评分- 外观
    SCORE_EXTERIOR = scrapy.Field()
    # 评分- 内饰
    SCORE_INTERIOR = scrapy.Field()
    # 评分- 性价比
    SCORE_COST_EFFECTIVE = scrapy.Field()

    # 评论的url
    COMMENT_URL = scrapy.Field()
    # 评论的内容
    COMMENT_CONTENT = scrapy.Field()

    # 有多少人支持这条口碑
    COMMENT_SUPPORT_QUANTITY = scrapy.Field()
    # 有多少人看过这条口碑
    COMMENT_SEEN_QUANTITY = scrapy.Field()