# -*- coding:utf-8 -*-
# @Time     : 2019-06-08 22:44
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : Calculating financial indicators

import time
import logging
import csv

from settings import data_path, pro


def calculate_roe(income):
    pass


def calculate_net_interest_rate(income):
    # 净利率=净利润/主营业务收入×100%=(利润总额-所得税费用)/主营业务收入*100%
    end_date = income['end_date']
    total_profit = float(income['total_profit'])
    income_tax = float(income['income_tax'])
    revenue = float(income['revenue'])
    net_interest_rate = (total_profit-income_tax)/revenue
    return end_date, net_interest_rate


def get_fina_indicator():
    df = pro.fina_indicator(ts_code='000040.SZ', start_date='20050101', end_date='20190630', fields='')
    file = data_path + '/test_data/fina_indicator_000040.SZ'+'.csv'
    df.to_csv(file)


def run():
    file = data_path + '/test_data/income_20190630_000040.SZ.csv'
    with open(file, newline='', encoding='UTF-8') as cf:
        reader = csv.DictReader(cf)
        for row in reader:
            end_date, net_interest_rate = calculate_net_interest_rate(row)
            print(end_date, '\t', net_interest_rate)


if __name__ == '__main__':
    run()
