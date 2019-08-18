# -*- coding:utf-8 -*-
# @Time     : 2019-06-08 21:04
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

import datetime

import tushare

from common.constant import data_path

tushare.set_token('1e431dd1d92959eeec4ef91f58a3ec1f85b5b242d32f1c3a2b00df08')
pro = tushare.pro_api()

data = pro.stock_basic(exchange='', list_status='L',
                       fields='ts_code,symbol,name,area,industry,fullname,enname,market,exchange,curr_type,'
                              'list_status,list_date,delist_date,is_hs')

today = datetime.datetime.today().strftime('%Y%m%d')
file = data_path+'/stock_basic/all_stock_list_'+today+'.csv'
data.to_csv(file)
print('Stocks saved.')
