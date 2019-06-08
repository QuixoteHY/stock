
import datetime

import tushare

from settings import data_path

# 1e431dd1d92959eeec4ef91f58a3ec1f85b5b242d32f1c3a2b00df08
tushare.set_token('1e431dd1d92959eeec4ef91f58a3ec1f85b5b242d32f1c3a2b00df08')
pro = tushare.pro_api()

# df = pro.income(ts_code='600000.SH', start_date='20100101', end_date='20180730',
#                 fields='ts_code,ann_date,f_ann_date,end_date,report_type,comp_type,basic_eps,diluted_eps')
df = pro.income(ts_code='600000.SH', start_date='20050101', end_date='20190730',
                fields='')

today = datetime.datetime.today().strftime('%Y%m%d')
file = data_path+'/income_'+today+'.csv'
df.to_csv(file)
print('Stocks saved.')
