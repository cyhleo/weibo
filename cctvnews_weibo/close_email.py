from scrapy.mail import MailSender
from scrapy import signals
from scrapy.exceptions import NotConfigured
import logging

class SendEmail(object):
    @classmethod
    def from_crawler(cls,crawler):
        return cls(crawler)
    def __init__(self,crawler):
        self.logger = logging.getLogger(__name__)
        self.crawler = crawler
        self.settings = crawler.settings
        crawler.signals.connect(self._spider_closed, signals.spider_closed)
        self.email_enable = crawler.settings.getbool('CLOSE_SPIDER_EMAIL_ENABLE')
        if not self.email_enable:
            raise NotConfigured
        self.smtpuser = crawler.settings.get('MAIL_USER')

    def _spider_closed(self,spider,reason):

        mailer = MailSender.from_settings(self.settings)
        stats_info = self.crawler.stats.get_stats(spider)

        body = "爬虫{}已经关闭，原因是: {}.\n以下为运行信息：\n {} " .format(spider.name, reason,stats_info,)
        subject = "[%s]爬虫关闭提醒" % spider.name
        try:
            return mailer.send(to={self.smtpuser},subject=subject,body=body)
        except Exception as e:
            self.logger.info(e,'发送邮件失败')