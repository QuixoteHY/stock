# -*- coding:utf-8 -*-
# @Time     : 2019-06-08 21:21
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

import time
import logging
import csv

from common.constant import data_path
from common.tushare_api import pro


def get_the_stock_history_income(_pro, ts_code, start_date='20050101', end_date='20190630', fields=''):
    # fields为空默认显示所有字段
    df = _pro.income(ts_code=ts_code, start_date=start_date, end_date=end_date, fields=fields)
    file = data_path+'/income/income_'+end_date+'_'+ts_code+'.csv'
    df.to_csv(file)


def run():
    date_str = '20190608'
    file = data_path + '/stock_basic/all_stock_list_' + date_str + '.csv'
    count = 0
    with open(file, newline='', encoding='UTF-8') as cf:
        reader = csv.DictReader(cf)
        for row in reader:
            count += 1
            try:
                get_the_stock_history_income(pro, row['ts_code'])
                print(str(count)+'\t', row['ts_code'], row['fullname'], '\t\t\t\t\t\t成功')
            except Exception as e:
                logging.info(logging.exception(e))
                print(str(count)+'\t', row['ts_code'], '\t\t失败')
                with open(data_path + '/err_log/err_income_' + date_str + '.log', 'a') as f:
                    f.write(row['ts_code']+'\n')
            time.sleep(2)


if __name__ == '__main__':
    # run()
    get_the_stock_history_income(pro, '000001.SZ')
    time.sleep(2)
    get_the_stock_history_income(pro, '000988.SZ')
    time.sleep(2)
    get_the_stock_history_income(pro, '002129.SZ')
    time.sleep(2)
    get_the_stock_history_income(pro, '601010.SH')
    time.sleep(2)
    get_the_stock_history_income(pro, '601799.SH')
