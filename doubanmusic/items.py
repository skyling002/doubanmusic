# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class LinkItem(scrapy.Item):
    tag = scrapy.Field()
    url = scrapy.Field()


class AlbumItem(scrapy.Item):
    # 基础信息（来源：专辑标题及网页URL）
    album_url = scrapy.Field()  # 当前页面URL
    album_name = scrapy.Field()  # 专辑名
    other_name = scrapy.Field() # 他名
    artist = scrapy.Field()  # 作者
    album_image = scrapy.Field()  # 专辑图片

    # 元数据（来源：专辑信息栏）
    tag = scrapy.Field()  # 流派
    release_date = scrapy.Field()  # 发行时间
    publisher = scrapy.Field()  # 出版方

    # 评分系统（来源：评分模块）
    rating = scrapy.Field()  # 综合评分
    rating_dist = scrapy.Field()  # 星级分布字典
    rating_count = scrapy.Field()  # 评分人数

    # 文本描述（来源：简介和曲目）
    dec = scrapy.Field()  # 简介文本
    tracks = scrapy.Field()  # 曲目列表

    # 关联内容（来源：相似推荐）
    similar_albums = scrapy.Field()  # 相似专辑列表，元素格式：{"name": "American Idiot", "rating":9.0}

    # 用户互动（来源：短评板块）
    short_reviews = scrapy.Field()  # 短评列表，元素格式：
    # {"user": "Miss Lucky", "content": "Wake Me Up...",
    #  "upvotes": 0, "time": "2008-04-23 08:57:11"}
