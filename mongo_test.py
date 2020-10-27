# -*- coding: utf-8 -*-
# @File    : mongo_test.py
# @Date    : 2020/10/22
# @Author  : HiCooper
# @Desc    :
from urllib.parse import quote_plus

from pymongo import MongoClient

if __name__ == '__main__':
    mongoClient = MongoClient('mongodb://user_qp_sp_new:%s@10.235.245.188:27017' % quote_plus('W4K+*fR11A6ayeBA'))
    col_list = mongoClient['qp_sp'].list_collection_names()
    print(col_list)
