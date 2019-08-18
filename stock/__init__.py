# -*- coding:utf-8 -*-
# @Time     : 2019-06-08 22:44
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

fina_indicators_dict = {
    # 资产负债比率(占总资产%)
    '现金与约当现金比率': dict(),
    '应收账款比率': dict(),
    '存货比率': dict(),
    '流动资产比率': dict(),
    '应付账款比率': dict(),
    '流动负债比率': dict(),
    '长期负债比率': dict(),
    '股东权益比率': dict(),
    '资产负债表平衡': dict(),
    # 五大财务比率
    # 财务结构
    '负债占资产比率': dict(),
    '长期资金占投资比率': dict(),
    # 偿债能力
    '流动比率': dict(),
    '速动比率': dict(),
    # 经营能力
    '应收账款周转率': dict(),

    '净利率': dict(),
}
fina_indicators_code = {
    # 资产负债比率(占总资产%)
    '现金与约当现金比率': "0001",
    '应收账款比率': "0002",
    '存货比率': "0003",
    '流动资产比率': "0004",
    '应付账款比率': "0005",
    '流动负债比率': "0006",
    '长期负债比率': "0007",
    '股东权益比率': "0008",
    '资产负债表平衡': "0009",
    # 五大财务比率
    # 财务结构
    '负债占资产比率': "00010",
    '长期资金占投资比率': "0011",
    # 偿债能力
    '流动比率': "0012",
    '速动比率': "0013",
    # 经营能力
    '应收账款周转率': "0014",

    '净利率': "0015",
}


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
