# -*- coding:utf-8 -*-
# @Time     : 2019-06-08 22:44
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : Calculating financial indicators

import copy
import csv

from settings import data_path, pro
from stock.utils import Utils
from stock.template.fina_indicators import get_table_code
from stock import fina_indicators_dict

fina_indicators = copy.deepcopy(fina_indicators_dict)


def calculate_cash_to_total_assets_rate(balancesheet):
    # 现金与约当现金比率=现金占总资产比率=(货币资金+交易性金融资产)/总资产*100%
    money_cap = float(balancesheet['money_cap'] if balancesheet['money_cap'] else 0)
    trad_asset = float(balancesheet['trad_asset'] if balancesheet['trad_asset'] else 0)
    total_assets = float(balancesheet['total_assets'] if balancesheet['total_assets'] else 0)
    cash_to_total_assets_rate = (money_cap+trad_asset)/total_assets
    return cash_to_total_assets_rate


def calculate_net_interest_rate(income):
    # 净利率=净利润/主营业务收入×100%=(利润总额-所得税费用)/主营业务收入*100%
    total_profit = float(income['total_profit'])
    income_tax = float(income['income_tax'])
    revenue = float(income['revenue'])
    net_interest_rate = (total_profit-income_tax)/revenue
    return net_interest_rate


def get_fina_indicator():
    df = pro.fina_indicator(ts_code='000040.SZ', start_date='20050101', end_date='20190630', fields='')
    file = data_path + '/test_data/fina_indicator_000040.SZ'+'.csv'
    df.to_csv(file)


def run():
    bs_file = data_path + '/test_data/balancesheet_20190630_000040.SZ.csv'
    ic_file = data_path + '/test_data/income_20190630_000040.SZ.csv'
    with open(bs_file, newline='', encoding='UTF-8') as bsf:
        # 资产负债表
        bs_reader = csv.DictReader(bsf)
        for row in bs_reader:
            # 现金与约当现金比率
            cash_to_total_assets_rate = calculate_cash_to_total_assets_rate(row)
            fina_indicators['现金与约当现金比率'][row['end_date']] = Utils.get_rate(cash_to_total_assets_rate)
    with open(ic_file, newline='', encoding='UTF-8') as icf:
        # 现金流量表
        ic_reader = csv.DictReader(icf)
        for row in ic_reader:
            # 净利率
            net_interest_rate = calculate_net_interest_rate(row)
            fina_indicators['净利率'][row['end_date']] = Utils.get_rate(net_interest_rate)
    get_table_code(fina_indicators)


if __name__ == '__main__':
    run()
