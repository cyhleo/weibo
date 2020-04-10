# 项目介绍
此项目用来爬取微博用户的公开信息，该项目以几个微博账户为起点，爬取他们各自的关注列表，爬取他们自己以及关注对象的所有微博。

# 部分结果展示
![](https://github.com/cyhleo/weibo/blob/master/image/weibo_info.png)
![](https://github.com/cyhleo/weibo/blob/master/image/weibo_acc.png)

# 项目说明
1. 使用scrapy框架来编写爬虫程序

2. 编写下载器中间件ProxyDownloaderMiddleware类，接入讯代理动态转发接口，实现ip切换。   
在setting中设置讯代理动态转发SECRET值和ORDERNO值。

3. 编写下载器中间件UserAgentDownloaderMiddleware类，使用fake_useragent库来随机获取User-Agent。

4. 编写下载器中间件CookiesMiddleware类，访问cookies池，随机获取cookies值，携带cookie进行访问。   
在settings中设置COOKIES_URL（cookies池网络接口）。

5. 编写下载器中间件ExceptionDownloaderMiddleware类，捕获状态码为4开头或者是5开头的响应，捕获所有的异常。   
在settings中设置该中间件的级别，该值应小于重试和重定向中间件的优先级。在下载器处理器返回响应到响应被调度器捕捉的过程中，保证ExceptionDownloaderMiddleware类的方法被最后执行。

6. 在settings中编写DEFAULT_REQUEST_HEADERS列表，构造包含Host、Accept-Encoding等信息的请求头。

7. 编写扩展Latencies类，实现每隔5秒测试一次吞吐量和响应延迟及处理延迟。    
在settings中设置LATENCIES_INTERVAL值（测试间隔时间）。

8. 编写扩展SendEmail类，实现在爬虫结束时，向邮箱发送爬虫停止的原因，以及StatsCollector中存储的信息。   
在settings中设置CLOSE_SPIDER_EMAIL_ENABLE值为True，设置MAIL_FROM值（邮件的发送者），
设置MAIL_HOST值（发送邮件的服务器），设置MAIL_USER值（邮箱用户名），设置MAIL_PASS值（发送邮箱的授权码），
设置MAIL_PORT值（端口号）。

9. 启用自动限速扩展，根据所爬网站的负载自动限制爬取速度。    
在seting中设置AUTOTHROTTLE_ENABLED值为True，设置AUTOTHROTTLE_START_DELAY（初始的下再延迟），
设置AUTOTHROTTLE_MAX_DELAY（最大下载延迟），AUTOTHROTTLE_TARGET_CONCURRENCY（发送到服务器的请求并发量）。

10. 使用scrapy_redis内置调度器类和请求去重类，使用redis集合作为消息队列数据结构，使用redis列表作为请求指纹存储的数据结构。   
在settings中设置SCHEDULER = 'scrapy_redis.scheduler.Scheduler'，DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'，
SCHEDULER_QUEUE_CLASS = 'scrapy_redis.queue.FifoQueue'    
在settings中设置REDIS_HOST、REDIS_PORT、REDIS_PASSWORD值（请求队列和去重指纹队列存储使用的redis数据库info）。

11. 通过解析json格式的响应内容，将非结构数据转化为结构化数据。

12. 编写中间件TimePipeline类，对item中created_at字段进行数据清洗，将‘分钟前’、‘小时前’、‘昨天’的时间格式
转换为’年-月-日 小时：分钟‘。

13. 编写pipeline MongoPipeline类，将下载的数据保存至MongoDB数据库。   
在settings中设置MONGO_URI值（mongodb的uri），设置MONGO_DATABASE值（数据库名）。

# 告示
本代码仅作学习交流，切勿用于商业用途。如涉及侵权，请邮箱联系，会尽快删除。
