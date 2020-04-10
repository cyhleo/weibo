# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import UserItem
from ..items import FllowItem
from ..items import WeiboItem

class WeiboCctvnewsSpider(scrapy.Spider):
    name = 'weibo_cctvnews'
    allowed_domains = ['m.weibo.cn']

    # 微博用户的主页
    user_url = 'https://m.weibo.cn/profile/info?uid={}'
    fllow_url = 'https://m.weibo.cn/api/container/getIndex?containerid=231051_-_followers_-_{}&page={}'
    weibo_url = 'https://m.weibo.cn/api/container/getIndex?containerid=230413{}_-_WEIBO_SECOND_PROFILE_WEIBO&page_type=03&page={}'
    def start_requests(self):
        # 将用户主页https://m.weibo.cn/profile/xxx 后的xxx的这串数字填入列表中
        for l in []:
            yield scrapy.Request(self.user_url.format(l),callback=self.parse_user)

    def parse_user(self, response):
        if response.url:
            json_data = json.loads(response.text)
            user = json_data.get('data').get('user')
            user_item = UserItem()
            field_map = {
                'uid':'id',
                'screen_name':'screen_name',
                'followers_count': 'followers_count',
                'follow_count': 'follow_count',
            }
            for field,attr in field_map.items():
                user_item[field] = user.get(attr)
            yield user_item
            uid = user.get('id')
            yield scrapy.Request(self.fllow_url.format(uid,1),callback=self.parse_fllow,meta={'page':1,'uid':uid})
            yield scrapy.Request(self.weibo_url.format(uid,1),callback=self.parse_weibo,meta={'page':1,'uid':uid})

    def parse_fllow(self,response):
        if response.url:
            page = response.meta.get('page')
            first_uid = response.meta.get('uid')
            json_data = json.loads(response.text)
            field_map = {
                'uid': 'id',
                'screen_name': 'screen_name',
                'followers_count': 'followers_count',
                'follow_count': 'follow_count'
            }
            if json_data.get('ok')==1 and json_data.get('data').get('cards') and len(json_data.get('data').get('cards')) and json_data.get('data').get('cards')[-1].get('card_group'):
                card_group = json_data.get('data').get('cards')[-1].get('card_group')

                for card in card_group:
                    if card.get("user"):
                        fllow_item = FllowItem()
                        for field,attr in field_map.items():
                            fllow_item[field] = card.get("user").get(attr)
                        uid = card.get("user").get('id')
                        yield fllow_item

                        yield scrapy.Request(self.weibo_url.format(uid, 1), callback=self.parse_weibo, meta={'page': 1,'uid':uid})
                page += 1
                yield scrapy.Request(self.fllow_url.format(first_uid,page),callback=self.parse_fllow,meta={'page':page,'uid':first_uid})



    def parse_weibo(self, response):
        if response.url:
            page = response.meta.get('page')
            uid_weibo = response.meta.get('uid')
            json_data = json.loads(response.text)

            field_map = {
                'id': 'id',
                'text': 'text',
                'raw_text': 'raw_text',
                'reposts_count': 'reposts_count',
                'comments_count': 'comments_count',
                'attitudes_count': 'attitudes_count',
                'created_at': 'created_at'
            }

            cards = json_data.get('data').get('cards')
            if json_data.get('ok')==1 and cards:
                for card in cards:
                    if card.get("mblog"):
                        weibo_item = WeiboItem()
                        for field, attr in field_map.items():
                            weibo_item[field] = card.get("mblog").get(attr)
                        pics = card.get("mblog").get('pics')
                        pic_url_list = []
                        if pics:
                            for pic in pics:
                                pic_url = pic.get('url')
                                pic_url_list.append(pic_url)
                        weibo_item['pics'] = pic_url_list
                        weibo_item['screen_name'] = card.get("mblog").get('user').get('screen_name')
                        yield weibo_item
                page += 1
                yield scrapy.Request(self.weibo_url.format(uid_weibo, page), callback=self.parse_weibo, meta={'page': page,'uid':uid_weibo})


