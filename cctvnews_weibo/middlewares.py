# -*- coding: utf-8 -*-

import json
import logging
import requests
from fake_useragent import UserAgent
import time
import hashlib
from twisted.internet import defer
from twisted.internet.error import TimeoutError, DNSLookupError, \
    ConnectionRefusedError, ConnectionDone, ConnectError, \
    ConnectionLost, TCPTimedOutError
from scrapy.http import HtmlResponse
from twisted.web.client import ResponseFailed
from scrapy.core.downloader.handlers.http11 import TunnelError


logger = logging.getLogger(__name__)

class ProxyMiddleware(object):
    '''
    接入讯代理动态转发接口，实现ip切换
    '''
    def __init__(self, secret, orderno):
        self.secret = secret
        self.orderno = orderno

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            secret=crawler.settings.get('SECRET'),
            orderno=crawler.settings.get('ORDERNO')
        )

    def process_request(self, request, spider):
        timestamp = str(int(time.time()))
        string = "orderno=" + self.orderno + "," + "secret=" + self.secret + "," + "timestamp=" + timestamp
        string = string.encode()
        md5_string = hashlib.md5(string).hexdigest()
        sign = md5_string.upper()
        auth = "sign=" + sign + "&" + "orderno=" + self.orderno + "&" + "timestamp=" + timestamp

        request.meta['proxy'] = 'http://forward.xdaili.cn:80'
        request.headers["Proxy-Authorization"] = auth
        logger.debug('正在使用动态转发')


class CookiesMiddleware(object):
    """访问cookies池，随机获取cookies值，携带cookie进行访问。"""
    def __init__(self, cookies_url):
        self.cookies_url = cookies_url

    def get_random_cookies(self):
        try:
            response = requests.get(self.cookies_url)
            if response.status_code == 200:
                cookies = json.loads(response.text)
                return cookies
        except requests.ConnectionError:
            return False

    def process_request(self, request, spider):
        logger.debug('正在获取Cookies')
        cookies = self.get_random_cookies()
        if cookies:
            request.cookies = cookies
            logger.debug('使用Cookies ' + json.dumps(cookies))

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(
            cookies_url=settings.get('COOKIES_URL')
        )


class UserAgentDownloaderMiddleware(object):
    """使用fake_useragent库来随机获取User-Agent"""
    def process_request(self, request, spider):
        agent = UserAgent()
        agent_one = agent.chrome
        logger.debug("user_agent:{}".format(agent_one))
        request.headers['User-Agent'] = agent_one


class ExceptionDownloaderMiddleware(object):
    ALL_EXCEPTIONS = (defer.TimeoutError, TimeoutError, DNSLookupError,
                           ConnectionRefusedError, ConnectionDone, ConnectError,
                           ConnectionLost, TCPTimedOutError, ResponseFailed,
                           IOError, TunnelError)


    def process_response(self,request,response,spider):
        if str(response.status).startswith('4') or str(response.status).startswith('5'):

            response = HtmlResponse(url='')
            logger.debug('{}got a response.status:{}'.format(request.url, response.status))
            return response
        return response

    def process_exception(self, request, exception, spider):
        if isinstance(exception,self.ALL_EXCEPTIONS):
            logger.debug('{}got a exception:{}'.format(request.url,exception))
            response = HtmlResponse(url='')
            return response

        logger.debug('{}got a exception:{},but not return response obj'.format(request.url, exception))

