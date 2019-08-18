# -*- coding:utf-8 -*-
# @Time     : 2019-06-08 22:44
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :


def format_to_mongodb(fina_indicators, ts_code):
    ts_code = ts_code.replace('.', '_')
    list_docs = list()
    for indicator_name, v in fina_indicators.items():
        for time, value in v.items():
            list_docs.append({'ts_code': ts_code,
                              'indicator_name': indicator_name,
                              'indicator_code': fina_indicators_code[indicator_name],
                              'time': time,
                              'indicator_value': value})
    return list_docs
