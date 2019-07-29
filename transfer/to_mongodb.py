# -*- coding:utf-8 -*-
# @Time     : 2019-07-29 11:08
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

from pymongo import MongoClient
import csv


# 创建连接MongoDB数据库函数
def connection():
    # 1:连接本地 MongoDB 数据库服务
    conn = MongoClient("localhost")
    # 2:连接本地数据库(stock)，没有时会自动创建
    db = conn.stock
    # 3:创建集合
    set1 = db.balancesheet
    # 4:看情况是否选择清空(两种清空方式，第一种不行的情况下，选择第二种)
    # 第一种直接remove
    set1.remove(None)
    # 第二种remove不好用的时候
    # set1.delete_many({})
    return set1


def insert_to_mongodb(set1):
    # 打开文件guazi.csv
    with open('../data/balancesheet/balancesheet_20190630_000001.SZ.csv', 'r', encoding='utf-8')as csvfile:
        # 调用csv中的DictReader函数直接获取数据为字典形式
        reader = csv.DictReader(csvfile)
        # 创建一个counts计数一下 看自己一共添加了了多少条数据
        counts = 0
        for each in reader:
            set1.insert(each)
            counts += 1
            print('成功添加了'+str(counts)+'条数据 ')


# 创建主函数
def main():
    set1 = connection()
    insert_to_mongodb(set1)


if __name__ == '__main__':
    main()
