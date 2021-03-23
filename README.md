SE_for_book
--------

本系统是关于图书的搜索引擎，内容是豆瓣图书中的部分标签下的内容（标签见下图）。

![image-20200814220029899](https://github.com/goodyong/SE_for_book/blob/master/image-20200814220029899.png)

需要条件
---------

elasticsearch [下载](https://www.elastic.co/cn/downloads/elasticsearch,"download")
(还可安装elasticsearch-head插件方便查看)

所需要的python包：elasticsearch，scrapy，flask

```shell
python -m pip install elasticsearch
python -m pip install scrapy
python -m pip install flask
```

运行方法
---------
(假设elasticsearch和elasticsearch-head都在es文件夹)

+ 首先运行elasticsearch：
  
  ```shell
    cd es\elasticsearch-7.8.1\bin
    ./elasticsearch
  ```

  或在es文件夹下双击elasticsearch.bat。elasticsearch默认运行于9200端口。

+ 可以运行elasticsearch-head用于查看数据（非必需）:
  
  需要已安装node.js
  
  ```shell
    cd es\elasticsearch-head
    npm run start
  ```
  
  elasricsearch-head默认运行于9100端口
  
+ 如果elasticsearch没有数据，则需要先运行一次爬虫，运行爬虫只需要执行DoubanReaderSpider目录下的main.py文件，或是: 

  ```shell
  cd DoubanReaderSpider
  scrapy crawl bookSpider
  ```

+ 爬取并存入ES后，可运行启动服务器运行搜索界面: 
  
  ```shell
  cd front_end
  python app.py
  ```
  
  然后按照提示打开浏览器访问即可使用。
