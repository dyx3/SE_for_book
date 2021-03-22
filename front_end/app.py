# coding:utf-8

from flask import request
from flask import Flask, render_template

import sys
sys.path.append('..')
from es.es_op import search_info, SIZE


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('/search.html')


@app.route('/search')
def search():
    keyword = request.args.get('wd')
    page = int(request.args.get('page')) - 1
    result, num, page_range = search_info(keyword, page * SIZE)
    return render_template('/result.html', data=result, num=num, wd=keyword,
                           start=page * 20, range=page_range, cur_page=page + 1)


@app.route('/user/<name>')
def user(name):
    return '<h1>hello,%s!' % name


if __name__ == '__main__':
    app.run()
