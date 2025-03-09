from lxml import etree

html = '''
<div id="info" class="ckd-collect" style="">
    <span class="pl">又名:</span>&nbsp;Ordeal by Pearls
    <br>
    <span style="">
        <span class="pl" style="">
            表演者:
            <a href="/search?q=%E9%AD%8F%E5%A6%82%E8%90%B1&amp;sid=37151690" style="">魏如萱</a>
            /
            <a href="/search?q=Waa+Wei&amp;sid=37151690" style="">Waa Wei</a>
        </span>
    </span>
    <br>
    <span class="pl">流派:</span>&nbsp;流行
    <br>
    <span class="pl" style="">专辑类型:</span>&nbsp;专辑
    <br>
    <span class="pl" style="">介质:</span>&nbsp;数字(Digital)
    <br>
    <span class="pl">发行时间:</span>&nbsp;2024-12-24
    <br>
    <span class="pl">出版者:</span>&nbsp;银翼文创有限公司 Mr. Wing Creative / 容合音乐
    <br>
</div>
'''

# 解析 HTML
tree = etree.HTML(html)

# 提取 id 为 info 的 div 里的所有文本
all_text = ''.join(tree.xpath('//*[@id="info"]//text()')).strip()
print(all_text)

# 定义分割关键词
keywords = ['又名:', '表演者:', '流派:', '专辑类型:', '介质:', '发行时间:', '出版者:']

# 用于存储提取的信息
info_dict = {}

# 依次处理每个关键词
for i in range(len(keywords)):
    keyword = keywords[i]
    start_index = all_text.find(keyword)
    if start_index != -1:
        start_index += len(keyword)
        if i < len(keywords) - 1:
            next_keyword = keywords[i + 1]
            end_index = all_text.find(next_keyword, start_index)
            if end_index == -1:
                end_index = len(all_text)
        else:
            end_index = len(all_text)
        value = all_text[start_index:end_index].strip()
        info_dict[keyword.rstrip(':')] = value

# 输出提取的信息
for key, value in info_dict.items():
    print(f"{key}: {value}")