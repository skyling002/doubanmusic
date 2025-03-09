# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

import csv
import logging


class DoubanmusicPipeline:
    def process_item(self, item, spider):
        return item


class AlbumPipeline:
    def __init__(self):
        # 打开 CSV 文件，使用 'utf-8' 编码并指定 newline='' 以避免 Windows 系统下的额外空行
        self.file = open('albums.csv', 'a', newline='', encoding='utf-8')
        # 定义 CSV 文件的字段名
        self.fieldnames = [
            'album_url', 'album_name', 'other_name', 'artist', 'album_image',
            'tag', 'release_date', 'publisher','rating', 'rating_dist',
            'rating_count', 'dec', 'tracks', 'similar_albums',
            'short_reviews'
        ]
        # 创建 CSV 写入器对象
        self.writer = csv.DictWriter(self.file, fieldnames=self.fieldnames)
        # 写入 CSV 文件的表头
        self.writer.writeheader()

    def process_item(self, item, spider):
        try:
            # 打印提取的数据
            logging.info(f"Extracted item: {item}")
            # 将数据写入 CSV 文件
            self.writer.writerow(item)
            return item
        except Exception as e:
            # 若出现异常，记录错误信息
            logging.error(f"Error processing item: {e}")
            return item

    def close_spider(self, spider):
        # 爬虫关闭时，关闭 CSV 文件
        self.file.close()