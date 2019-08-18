# -*- coding:utf-8 -*-
# @Time     : 2019-08-18 16:24
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

import csv

from common.constant import data_path


class Controller(object):
    def __init__(self):
        self.balance_sheet_data_path_model = data_path + '/balancesheet/balancesheet_20190630_%s.csv'

    def get_balance_sheet(self, ts_code):
        # 资产负债表
        with open(self.balance_sheet_data_path_model % ts_code, newline='', encoding='UTF-8') as bsf:
            bs_reader = csv.DictReader(bsf)
            for row in bs_reader:
                pass

    def get_fina_indicators(self, ts_code):
        pass
