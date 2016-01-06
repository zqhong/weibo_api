# -*- coding: utf-8 -*-

"""
    @author akira <i@zqhong.com>
    @date   2016-01-06
"""

from weibo import *
import os.path

if __name__ == '__main__':
    weibo_obj = "weibo.dill"
    if os.path.exists(weibo_obj):
        with open(weibo_obj) as f:
            weibo = dill.load(f)
    else:
        weibo = Weibo()

    weibo = Weibo()
    weibo.post("test post by wei_api")

    with open(weibo_obj, "w") as f:
        dill.dump(weibo, f)
