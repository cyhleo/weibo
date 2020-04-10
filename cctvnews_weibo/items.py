# -*- coding: utf-8 -*-
import scrapy


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    collection = 'user_info'
    uid = scrapy.Field()
    #用户名称
    screen_name = scrapy.Field()
    #用户描述
    # description = scrapy.Field()
    #粉丝数量
    followers_count = scrapy.Field()
    #关注人数
    follow_count = scrapy.Field()

class WeiboItem(scrapy.Item):
    # define the fields for your item here like:
    collection = 'weibos'
    # 用户名称
    screen_name = scrapy.Field()
    # id号
    id = scrapy.Field()
    text = scrapy.Field()
    # 微博内容
    raw_text = scrapy.Field()
    # 转发数 评论数 点赞数
    reposts_count = scrapy.Field()
    comments_count = scrapy.Field()
    attitudes_count = scrapy.Field()
    #图片url列表
    pics = scrapy.Field()
    #发布时间
    created_at = scrapy.Field()
class FllowItem(scrapy.Item):
    collection = 'user_info'
    uid = scrapy.Field()
    #微博名
    screen_name = scrapy.Field()
    #粉丝数
    followers_count = scrapy.Field()
    #关注人数
    follow_count = scrapy.Field()

