api包: 主要是实现http服务器，提供api接口(通过get请求,返回json数据)
    apiServer.py

data文件夹: 主要是数据库文件的存储位置和qqwry.dat(可以查询ip的地理位置)
    qqwry.dat

spider包: 主要是爬虫的核心功能，爬取代理网站上的代理ip
    HtmlDownloader.py
    HtmlPraser.py
    ProxyCrawl.py

test包: 测试一些用例，不参与整个项目的运行

util包: 提供一些工具类
    IPAddress.py    查询ip的地理位置
    logger.py
    compatibility.py
    exception.py
    SqlHelper.py

validator包: 用来测试ip地址是否可用
    Validator.py

config.py: 主要是配置信息(包括配置ip地址的解析方式和数据库的配置)

IPProxy.py: 主文件