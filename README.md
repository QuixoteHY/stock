# stock
目前已实现功能：A股上市公司部分财务信息查询。

数据源：Tushare

使用MongoDB做数据存储，使用aiohttp做web查询接口

使用：http://119.29.152.194:8888/get/stock/fina_indicators/ + A股股票代码
例子：http://119.29.152.194:8888/get/stock/fina_indicators/600699

export PYTHONPATH=/home/ubuntu/myproject/stock:$PYTHONPATH
