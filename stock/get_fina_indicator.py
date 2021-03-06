# -*- coding:utf-8 -*-
# @Time     : 2019-06-09 15:38
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : fina_indicator

import time
import logging
import csv

from common.constant import data_path
from common.tushare_api import pro


def get_the_stock_history_fina_indicator(_pro, ts_code, start_date='20050101', end_date='20190630', fields=''):
    # fields为空默认显示所有字段
    df = _pro.fina_indicator(ts_code=ts_code, start_date=start_date, end_date=end_date, fields=fields)
    file = data_path+'/fina_indicator/fina_indicator_'+end_date+'_'+ts_code+'.csv'
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
                get_the_stock_history_fina_indicator(pro, row['ts_code'])
                print(str(count)+'\t', row['ts_code'], row['fullname'], '\t\t\t\t\t\t成功')
            except Exception as e:
                logging.info(logging.exception(e))
                print(str(count)+'\t', row['ts_code'], '\t\t失败')
                with open(data_path + '/err_log/err_fina_indicator_' + date_str + '.log', 'a') as f:
                    f.write(row['ts_code']+'\n')
            time.sleep(2)


def repair():
    date_str = '20190608'
    file = data_path + '/err_log/err_fina_indicator_' + date_str + '.log'
    count = 0
    with open(file, encoding='UTF-8') as f:
        for line in f:
            ts_code = line.strip()
            if not ts_code:
                continue
            count += 1
            try:
                get_the_stock_history_fina_indicator(pro, ts_code)
                print(str(count)+'\t', ts_code, '\t\t成功')
            except Exception as e:
                logging.info(logging.exception(e))
                print(str(count)+'\t', ts_code, '\t\t失败')
                with open(data_path + '/err_log/err_fina_indicator_20190609.log', 'a') as f_err:
                    f_err.write(ts_code+'\n')
            time.sleep(2)


if __name__ == '__main__':
    # run()
    repair()
