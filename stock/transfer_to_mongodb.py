# -*- coding:utf-8 -*-
# @Time     : 2019-06-20 22:20
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

import csv

from common.constant import data_path
from common.utils import Utils


data = list()


def transfer_to_mongodb(stock_basic):
    ts_code = stock_basic['ts_code']
    bs_file = data_path + '/balancesheet/balancesheet_20190630_%s.csv' % ts_code
    ic_file = data_path + '/income/income_20190630_%s.csv' % ts_code
    cf_file = data_path + '/cashflow/cashflow_20190630_%s.csv' % ts_code
    fi_file = data_path + '/fina_indicator/fina_indicator_20190630_%s.csv' % ts_code
    financial_statements = dict()
    with open(bs_file, newline='', encoding='UTF-8') as bsf:
        # 资产负债表
        bs_reader = csv.DictReader(bsf)
        for row in bs_reader:
            row = dict(row)
            if row['end_date'] not in financial_statements:
                financial_statements[row['end_date']] = {'balance_sheet': dict(), 'income': dict(),
                                                         'cash_flow': dict(), 'fifi': dict(), }
            financial_statements[row['end_date']]['balance_sheet'] = row
    with open(ic_file, newline='', encoding='UTF-8') as icf:
        # 利润表
        ic_reader = csv.DictReader(icf)
        for row in ic_reader:
            row = dict(row)
            if row['end_date'] not in financial_statements:
                financial_statements[row['end_date']] = {'balance_sheet': dict(), 'income': dict(),
                                                         'cash_flow': dict(), 'fifi': dict(), }
            financial_statements[row['end_date']]['income'] = row
    with open(cf_file, newline='', encoding='UTF-8') as cff:
        # 现金流量表
        cf_reader = csv.DictReader(cff)
        for row in cf_reader:
            row = dict(row)
            if row['end_date'] not in financial_statements:
                financial_statements[row['end_date']] = {'balance_sheet': dict(), 'income': dict(),
                                                         'cash_flow': dict(), 'fifi': dict(), }
            financial_statements[row['end_date']]['cash_flow'] = row
    with open(fi_file, newline='', encoding='UTF-8') as fif:
        # 财务指标
        fi_reader = csv.DictReader(fif)
        for row in fi_reader:
            row = dict(row)
            if row['end_date'] not in financial_statements:
                financial_statements[row['end_date']] = {'balance_sheet': dict(), 'income': dict(),
                                                         'cash_flow': dict(), 'fifi': dict(), }
            financial_statements[row['end_date']]['fifi'] = row
    # print({'_id': ts_code, 'financial_statements': financial_statements})
    data.append({'_id': ts_code, 'financial_statements': financial_statements, 'stock_basic': stock_basic})


def run():
    mongodb_fi = Utils.get_conn_fi()
    date_str = '20190608'
    file = data_path + '/stock_basic/all_stock_list_' + date_str + '.csv'
    count = 0
    with open(file, newline='', encoding='UTF-8') as cf:
        reader = csv.DictReader(cf)
        for row in reader:
            count += 1
            try:
                transfer_to_mongodb(row)
                print(str(count)+'\t', row['ts_code'], row['fullname'], '\t\t\t\t\t\t成功')
            except Exception as e:
                print(e)
                print(str(count)+'\t', row['ts_code'], '\t\t失败')
                with open(data_path + '/err_log/err_income_' + date_str + '.log', 'a') as f:
                    f.write(row['ts_code']+'\n')
    # mongodb_fi.insert(data)
    count = 0
    for c in data:
        count += 1
        print(count)
        mongodb_fi.insert(c)


if __name__ == '__main__':
    run()
