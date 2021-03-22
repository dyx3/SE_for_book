# -*- coding: UTF-8 -*-
from elasticsearch import Elasticsearch

# 连接elasticsearch
es = Elasticsearch(hosts='http://localhost:9200/', maxsize=25)

# 采用ik_max_word模式进行分词的映射
max_word_mapping = {
    "mappings": {
        "properties": {
            "author": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                },
                "analyzer": "ik_max_word"
            },
            "binding": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                },
                "analyzer": "ik_max_word"
            },
            "intro": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                },
                "analyzer": "ik_max_word"
            },
            "isbn": {
                "type": "keyword"
            },
            "name": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                },
                "analyzer": "ik_max_word"
            },
            "page_num": {
                "type": "long"
            },
            "price": {
                "type": "float"
            },
            "publisher": {
                "type": "keyword"
            },
            "score": {
                "type": "float"
            },
            "series": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                },
                "analyzer": "ik_max_word"
            },
            "url": {
                "type": "keyword"
            }
        }
    }
}

# 采用ik_smart模式进行分词的映射
smart_mapping = {
    "mappings": {
        "properties": {
            "author": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                },
                "analyzer": "ik_smart"
            },
            "binding": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                },
                "analyzer": "ik_smart"
            },
            "intro": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                },
                "analyzer": "ik_smart"
            },
            "isbn": {
                "type": "keyword"
            },
            "name": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                },
                "analyzer": "ik_smart"
            },
            "page_num": {
                "type": "long"
            },
            "price": {
                "type": "float"
            },
            "publisher": {
                "type": "keyword"
            },
            "score": {
                "type": "float"
            },
            "series": {
                "type": "text",
                "fields": {
                    "keyword": {
                        "type": "keyword",
                        "ignore_above": 256
                    }
                },
                "analyzer": "ik_smart"
            },
            "url": {
                "type": "keyword"
            }
        }
    }
}


# 创建一个名为index的索引, 映射是给定的两种之一, 由if_ik_smart指定
def create_index(index, if_ik_smart=True):
    # 若原来存在此索引，先删除
    res = es.indices.delete(index=index, ignore=[400, 404])
    print('del--', res)
    if if_ik_smart:
        res = es.indices.create(index=index, ignore=[400, 404], body=smart_mapping)
    else:
        res = es.indices.create(index=index, ignore=[400, 404], body=max_word_mapping)
    print('create--', res)


# 向指定的索引index插入数据item
def insert(index, item):
    res = es.index(index=index, doc_type='_doc', body=item, ignore=[400, 409])
    print('insert--', res)
    return res


# 每一页的结果数上限
SIZE = 20


# 查询
# 返回[当前页号对应的结果列表, 结果总数, 总页数]
def search_info(keyword, start):
    results_list = []
    print(start)
    count_query = {
        "query": {
            "multi_match": {
                "query": keyword,
                # 提升了查询时一些字段的权重
                "fields": ["name^7", "author^3", "series", "binding", "publisher", "intro^5"]
            }
        }
    }
    query = {
        "query": {
            "multi_match": {
                "query": keyword,
                # 提升了查询时一些字段的权重
                "fields": ["name^7", "author^3", "series", "binding", "publisher", "intro^5"]
            }
        },
        "size": SIZE,
        "from": int(start)
    }
    print(query)
    # 结果总数
    res = es.count(index='book', doc_type='_doc', ignore=[400, 404],
                   body=count_query)
    print(res)
    count = res['count']
    # 结果
    res = es.search(index='book', doc_type='_doc', ignore=[400, 404],
                    body=query)
    print(res)
    if 0 != res['hits']['total']['value']:
        for hit in res['hits']['hits']:
            print(hit)
            name = hit['_source']['name']
            author = hit['_source']['author']
            isbn = hit['_source']['isbn']
            binding = hit['_source']['binding']
            page_num = hit['_source']['page_num']
            publisher = hit['_source']['publisher']
            price = hit['_source']['price']
            series = hit['_source']['series']
            url = hit['_source']['url']
            score = hit['_source']['score']
            intro = hit['_source']['intro'] if len(hit['_source']['intro']) < 400 \
                else (hit['_source']['intro'][0:400] + '...')
            results_list.append(
                {'name': name,
                 'score': score,
                 'author': author,
                 'publisher': publisher,
                 'isbn': isbn,
                 'binding': binding,
                 'series': series,
                 'price': price,
                 'url': url,
                 'page_num': page_num,
                 'intro': intro})
    return results_list, count, int(count / 20) + 1
