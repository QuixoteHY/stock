
from os.path import dirname

import tushare

data_path = dirname(__file__)+'/data'

tushare.set_token('1e431dd1d92959eeec4ef91f58a3ec1f85b5b242d32f1c3a2b00df08')
pro = tushare.pro_api()
