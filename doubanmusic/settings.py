# Scrapy settings for doubanmusic project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

TUNNEL = 'i528.kdltps.com:15818'
TUNNEL_USERNAME = 't14186799080081'
TUNNEL_PASSWORD = 'w7xvgxeb'


BOT_NAME = "doubanmusic"

SPIDER_MODULES = ["doubanmusic.spiders"]
NEWSPIDER_MODULE = "doubanmusic.spiders"



# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
#
# # TODO UA列表和代理IP列表
# USER_AGENTS = [
#        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36...',
#        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...',
#        # 准备 50+ 真实浏览器 UA
#    ]

# PROXY_LIST = [
#     "",
# ]

# 在settings.py中配置
REDIRECT_MAX_TIMES = 5  # 限制重定向次数

# Obey robots.txt rules
ROBOTSTXT_OBEY = False # 不遵循robots协议


# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 5  # 全局并发数设置为代理隧道的最大并发数

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 3  # 基础延迟
RANDOMIZE_DOWNLOAD_DELAY = True  # 添加±0.5秒随机波动

# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN = 2  # 每个域名的并发请求数
# CONCURRENT_REQUESTS_PER_IP = 2  # 每个 IP 的并发请求数

# 启用自动限速扩展
AUTOTHROTTLE_ENABLED = True
# 初始下载延迟
AUTOTHROTTLE_START_DELAY = 5
# 最大下载延迟
AUTOTHROTTLE_MAX_DELAY = 60
# 目标平均响应时间
AUTOTHROTTLE_TARGET_CONCURRENCY = 2.0
# 显示自动限速统计信息
AUTOTHROTTLE_DEBUG = False
# Disable cookies (enabled by default)
COOKIES_ENABLED = False # 不需要模拟登录

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "doubanmusic.middlewares.DoubanmusicSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
    # "doubanmusic.middlewares.ProxyMiddleware": 543,
    "doubanmusic.middlewares.UserAgentMiddleware": 544,
   # "doubanmusic.middlewares.DoubanmusicDownloaderMiddleware": 543,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
   # "doubanmusic.pipelines.DoubanmusicPipeline": 300,
    "doubanmusic.pipelines.AlbumPipeline": 300,
}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
AUTOTHROTTLE_ENABLED = True
# The initial download delay
AUTOTHROTTLE_START_DELAY = 5  # 初始延迟
# The maximum download delay to be set in case of high latencies
AUTOTHROTTLE_MAX_DELAY = 15   # 最大延迟（服务器响应慢时自动延长）
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
