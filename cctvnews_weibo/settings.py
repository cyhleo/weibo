# -*- coding: utf-8 -*-

# Scrapy settings for cctvnews_weibo project

BOT_NAME = 'cctvnews_weibo'

SPIDER_MODULES = ['cctvnews_weibo.spiders']
NEWSPIDER_MODULE = 'cctvnews_weibo.spiders'

# 设置请求头
DEFAULT_REQUEST_HEADERS = {
    'Accept': 'application/json, text/plain, */*',
    'accept-encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'x-requested-with': 'XMLHttpRequest',
}

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# 设置并发请求数
CONCURRENT_REQUESTS =
CONCURRENT_REQUESTS_PER_DOMAIN =
CONCURRENT_REQUESTS_PER_IP =

EXTENSIONS = {
    'cctvnews_weibo.latencies.Latencies':500,
    'cctvnews_weibo.close_email.SendEmail':500
}

LATENCIES_INTERVAL = 5


CLOSE_SPIDER_EMAIL_ENABLE = True

# 邮件发送者
MAIL_FROM = '383209685@qq.com'
# 发送邮件的服务器
MAIL_HOST = 'smtp.qq.com'
# 用户名
MAIL_USER = '383209685@qq.com'
# 发送邮箱的授权码
MAIL_PASS = 'ywerzpwfgqkmbihd'
MAIL_PORT = 465
MAIL_TLS=True
MAIL_SSL=True

LOG_ENABLED = True
LOG_ENCODING = 'utf-8'

#logger输出格式设置
LOG_FORMATTER = 'scrapy.logformatter.LogFormatter'
LOG_FORMAT = '%(asctime)s [%(name)s] %(levelname)s: %(message)s'
LOG_DATEFORMAT = '%Y-%m-%d %H:%M:%S'

# 如果为True，则进程的所有标准输出（和错误）将重定向到日志。 例如，如果您打印（'hello'）它将出现在Scrapy日志中。
LOG_STDOUT = True

# 显示的日志最低级别
LOG_LEVEL = 'INFO'

import datetime
t = datetime.datetime.now()
log_file_path = './log_{}_{}_{}.log'.format(t.year, t.month,t.day)
# log磁盘保存地址
LOG_FILE = log_file_path


# 开启自动限速设置
AUTOTHROTTLE_ENABLED = True

# 设置最小的下载延迟时间
DOWNLOAD_DELAY =

# The initial download delay
AUTOTHROTTLE_START_DELAY = 5

# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 60

# 发送到每一个服务器的并行请求数量
AUTOTHROTTLE_TARGET_CONCURRENCY =
# Enable showing throttling stats for every response received:

# 是否开启调试模式，将显示收到的每个响应的统计信息，
# 以便观察到延迟发送请求的时间如何一步步被调整
AUTOTHROTTLE_DEBUG = False



DOWNLOADER_MIDDLEWARES = {
    'cctvnews_weibo.middlewares.CookiesMiddleware': 554,
    'cctvnews_weibo.middlewares.ProxyMiddleware': 555,
    'cctvnews_weibo.middlewares.UserAgentDownloaderMiddleware': 556,
    'cctvnews_weibo.middlewares.ExceptionDownloaderMiddleware': 100,
}

SECRET = '87ac92a36ec84f5596098679bac93915'
ORDERNO = 'ZF201910112450U6iATq'

ITEM_PIPELINES = {
    'cctvnews_weibo.pipelines.TimePipeline': 300,
    'cctvnews_weibo.pipelines.MongoPipeline': 301,
}


MONGO_URI = 'localhost'

MONGO_DATABASE = 'weibo_cnnews_new'

COOKIES_URL = 'http://localhost:5000/weibo/random'


# 在爬虫结束的时候不清空请求队列和去重指纹队列
SCHEDULER_PERSIST = True
# 在爬虫开始的时候不清空请求队列
SCHEDULER_FLUSH_ON_START = False
# 启用scrapy_redis内置的调度器
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
# 启动scrapy_redis内置的请求去重类
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
# 启用scrapy_redis内置的先进先出队列
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'

#请求队列和去重指纹队列存储使用的redis数据库info
REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_PASSWORD = None

# 布尔值，指定是否 启用telnet控制台（
TELNETCONSOLE_ENABLED = True
# 用于telnet控制台的端口范围。如果设置为None或0，则使用动态分配的端口。
TELNETCONSOLE_PORT = [6023, 6073]
TELNETCONSOLE_HOST = '127.0.0.1'
# telnet连接认证的用户名
TELNETCONSOLE_USERNAME = 'scrapy'
# telnet连接认证的密码
TELNETCONSOLE_PASSWORD = 'pd'

