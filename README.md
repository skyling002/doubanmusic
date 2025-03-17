## 参数说明
- `settings.py`: 项目设置文件，由于并发设置极小，所以速度很慢，如需优化，请修改`settings.py`文件中的`CONCURRENT_REQUESTS`参数。

## 代理IP
- 代理管道默认关闭，如需开启代理管道，请修改`settings.py`文件中的`PROXY_ENABLED`参数为`True`。
![img.png](doubanmusic/img.png)
- 还需在Middleware.py中ProxyMiddleware类添加代理服务器配置。
![img_1.png](doubanmusic/img_1.png)

## 运行说明
- 运行项目时，请确保已安装Python环境，并安装相关依赖库。
- run.py 文件为项目主入口，负责启动爬虫。

## 数据文件
描述项目中使用的数据文件及其用途。

- `albums.csv`: 专辑数据文件。
- `albums01.csv`: 新增的专辑数据文件。

## 日志文件
描述项目中生成的日志文件及其用途。

- `scrapy.log`: 爬虫运行日志。

## 代码结构
简要介绍代码的主要模块和功能。

- `doubanmusic/`: 项目主目录。
  - `middlewares.py`: 中间件配置。
  - `pipelines.py`: 数据处理管道。
  - `settings.py`: 项目设置。
  - `spiders/`: 爬虫模块。
    - `music_spider.py`: 音乐专辑爬虫。
  - `utils/`: 工具模块。
    - `entity.py`: 实体处理工具。
    - `function.py`: 功能函数。

## 联系

