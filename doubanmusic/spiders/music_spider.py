import logging
import re
import time

import scrapy
from scrapy.exceptions import IgnoreRequest

from doubanmusic.items import AlbumItem
from doubanmusic.utils.entity import keywords
from doubanmusic.utils.function import split_text, split_short_reviews


class MusicSpiderSpider(scrapy.Spider):
    name = "music_spider"
    allowed_domains = ["music.douban.com"]
    start_urls = ["https://music.douban.com/tag/"]
    douban_url = "https://music.douban.com"
    album_base_url = "https://music.douban.com/subject/"
    tag_base_url = "https://music.douban.com/tag/"
    tag_urls = []
    album_urls = []
    MAX_PAGES = 50
    ITEM_PER_PAGE = 20
    index = 0
    skip = 0

    # 配置日志
    logging.basicConfig(
        filename='scrapy.log',
        format='%(levelname)s: %(message)s',
        level=logging.INFO,
        encodings='utf-8'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 记录爬虫开始时间
        self.start_time = time.time()

    def closed(self, reason):
        end_time = time.time()
        # 计算爬虫运行时长
        duration = end_time - self.start_time
        logging.info(f"爬虫运行时长: {duration} 秒，结束原因: {reason}")
        # 爬虫关闭时打印自定义日志
        logging.info("爬虫关闭，正在保存数据...")
        logging.info(f'一共跳过{self.skip}个专辑')
        logging.info(f'共爬取{self.index}个专辑')

    def parse(self, response):
        """处理分类列表页，提取所有分类URL"""
        list_td = response.xpath('//*[@id="风格"]/div[2]//td')
        for td in list_td:
            tag = td.xpath('./a/text()').get()
            tag_url = self.tag_base_url + tag
            self.tag_urls.append(tag_url)

        for index, tag_url in enumerate(self.tag_urls):
            self.logger.info(f"正在爬取分类: {tag_url}")
            yield response.follow(tag_url, self.parse_category)

    def parse_category(self, response):
        """处理单个分类页的分页逻辑"""
        # 先提取当前分类页的专辑URL
        subject_list = response.xpath('//*[@id="subject_list"]/table/tr[@class="item"]')
        if subject_list == []:
            self.logger.info(f"该分类已无专辑")
            return
        for subject in subject_list:
            album_id = subject.xpath('./@id').get()
            has_rating = subject.xpath('.//div[contains(@class,"star") and contains(@class,"clearfix")]')
            if not has_rating:
                self.logger.debug(f"跳过无评分专辑: {album_id}")
                self.skip += 1
                continue
            album_url = self.album_base_url + album_id
            self.album_urls.append(album_url)
            self.logger.info(f"正在爬取专辑: {album_id}")
            self.index += 1
            yield response.follow(album_url, self.parse_album)

        # # 处理分页（示例最多爬取50页）
        next_page = response.xpath('//span[@class="next"]/a/@href').get()
        if not next_page:
            logging.info("未找到下一页，即将返回爬取下一个分类")

        next_url = self.douban_url + next_page
        logging.info("下一页: %s", next_url)
        yield response.follow(next_url, self.parse_category)

    def parse_album(self, response):
        item = AlbumItem()
        item['album_url'] = response.url
        item['album_name'] = response.xpath('//*[@id="wrapper"]/h1/span/text()').get().strip()
        item['album_image'] = response.xpath('//*[@id="mainpic"]/span/a/img/@src').get().strip()

        # 提取 id 为 info 的元素内的所有文本
        album_info_list = response.xpath('//*[@id="info"]//text()').getall()
        # 将文本列表拼接成一个字符串
        album_info = ''.join(album_info_list)
        info_dict = split_text(keywords, album_info)
        # 提取出版者
        item['artist'] = info_dict.get('表演者:', '').replace(' ','')
        item['publisher'] = info_dict.get('出版者:', '')
        item['other_name'] = info_dict.get('又名:', '')
        item['tag'] = info_dict.get('流派:', '')
        item['release_date'] = info_dict.get('发行时间:', '')

        # 提取评分
        # 定位到 <strong> 标签
        rating_element = response.xpath('//div[@id="interest_sectl"]//strong[@class="ll rating_num"]')
        # 提取 <strong> 标签内的文本内容
        rating_text = rating_element.xpath('text()').get()
        if rating_text:
            # 去除首尾空格
            rating = rating_text.strip()
            try:
                # 尝试将评分转换为浮点数
                item['rating'] = float(rating)
            except ValueError:
                # 若转换失败，将评分设为 None
                item['rating'] = None
        else:
            # 若未提取到评分文本，将评分设为 None
            item['rating'] = None

        # 直接在 xpath 中提取 span 标签内的文本内容
        rating_count_text = response.xpath('//div[@id="interest_sectl"]//div[@class="rating_sum"]/a/span/text()').get()
        if rating_count_text:
            # 去除首尾空格
            rating_count_str = rating_count_text.strip()
            try:
                # 尝试将评分人数转换为整数
                item['rating_count'] = int(rating_count_str)
            except ValueError:
                # 若转换失败，将评分人数设为 None
                item['rating_count'] = None
        else:
            # 若未提取到评分人数文本，将评分人数设为 None
            item['rating_count'] = None

        # 描述
        dec_elements = response.xpath('//*[@id="link-report"]/span[1]/span')
        if dec_elements:
            # 获取所有元素的文本内容
            dec_texts = dec_elements.getall()
            # 将文本列表用换行符连接成一个字符串
            combined_text = '\n'.join(dec_texts)
            # 使用正则表达式去除多余的换行符和回车符
            cleaned_text = re.sub(r'[\r\n]+', '\n', combined_text).strip()
            item['dec'] = cleaned_text
        else:
            item['dec'] = ''

        # 提取曲目列表
        tracks = []
        track_lis = response.xpath('//div[@id="content"]//div[contains(@class, "track-list")]//li')
        for li in track_lis:
            # 假设曲目名称在 li 标签内的文本中，提取并去除首尾空白字符
            track_name = li.xpath('text()').get()
            if track_name:
                track_name = track_name.strip()
                if track_name:
                    tracks.append(track_name)

        # 将提取的曲目列表赋值给 item 中的 'tracks' 字段
        item['tracks'] = tracks

        # 提取相似专辑
        # item['similar_albums'] =

        # 提取短评
        # 获取所有 li 元素
        lis = response.xpath('//*[@id="new_score"]//li')
        short_reviews = split_short_reviews(lis)
        item['short_reviews'] = short_reviews
        yield item




