
import datetime

import tushare

from settings import data_path

# Step 1. Get stocks online
stocks_raw_data = tushare.get_stock_basics()
stocks = stocks_raw_data.index.tolist()

# Step 2. Save the stocks list to a local file
today = datetime.datetime.today().strftime('%Y%m%d')
file = data_path+'/all_stock_list_'+today+'.csv'
stocks_raw_data.to_csv(file)
print('Stocks saved.')


