from doubanmusic.utils.entity import rating_mapping

# 根据关键词分割文本
def split_text(keywords, text):
    info_dict = {}
    for i in range(len(keywords)):
        keyword = keywords[i]
        start_index = text.find(keyword)
        if start_index != -1:
            start_index += len(keyword)
            if i < len(keywords) - 1:
                next_keyword = keywords[i + 1]
                end_index = text.find(next_keyword, start_index)
                if end_index == -1:
                    end_index = len(text)
            else:
                end_index = len(text)
            value = text[start_index:end_index].strip()
            # 去除两端多余空格和换行符
            value = value.replace('\n', '').replace('\r', '').strip()
            info_dict[keyword] = value if value else ''
    return info_dict

# 提取短评
def split_short_reviews(lis):
    short_reviews = []
    for li in lis:
        # 使用相对路径获取用户名，避免使用绝对路径
        username_element = li.xpath('./div/h3/span[2]/a')
        username = username_element.xpath('text()').get() if username_element else None

        # 使用相对路径获取评分标签，避免使用绝对路径，并处理可能的 None 值
        rating_flag_element = li.xpath('./div/h3/span[2]/span[1]')
        rating_flag = rating_flag_element.xpath('@title').get()
        rating_flag = rating_flag.strip() if rating_flag else None

        # 根据评分标签获取对应的评分值
        user_rating = rating_mapping.get(rating_flag, 0)
        user_views = li.xpath('./div/p/span/text()').get().strip()
        short_reviews.append({
            'username': username,
            'rating': user_rating,
            'views': user_views,
        })
    return short_reviews