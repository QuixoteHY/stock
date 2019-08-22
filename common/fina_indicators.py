# -*- coding:utf-8 -*-
# @Time     : 2019-06-12 23:21
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

from common.data_model import asset_liability_rate
from common.data_model import financial_structure
from common.data_model import solvency
from common.data_model import business_capability
from common.data_model import profitability
from common.data_model import cash_flow


def get_table_html(fina_indicators, category_name, category_list):
    html = """
<table class="fina_indicators" border="4" style="font-size:13px">
    <caption style="color:blue;font-weight:bold;font-size:15px"><i>%s</i></caption>
    %s
</table>
    """
    year_list = ['20' + str(i) + '1231' for i in range(10, 19)]
    table = '<tr style="font-weight:bold;font-size:15px"><td align=center>类别</td>'
    table = table + '\n'.join(['<td align=center>' + year + '</td>' for year in year_list]) + '</tr>'
    header_print = '类别' + 11 * ' ' + '  '.join(year_list)
    print(header_print)
    for indicator_name in category_list:
        indicators = fina_indicators[indicator_name]
        tr_indicator = '<tr><td align=center>' + indicator_name + '</td>'
        temp_string = indicator_name + (20 - len(indicator_name) * 2) * ' ' + '\t'
        for year in year_list:
            if year in indicators:
                tr_indicator = tr_indicator + '<td>' + str(indicators[year]) + '</td>'
                temp_string = temp_string + str(indicators[year]) + (10 - len(str(indicators[year]))) * ' '
            else:
                tr_indicator = tr_indicator + '<td>--</td>'
                temp_string = temp_string + '' + (10 - len('')) * ' '
        tr_indicator += '</tr>'
        table += tr_indicator
        print(temp_string)
    return html % (category_name, table)


def get_html_table_code(fina_indicators, stock_basic):
    stock_basic_html = """
<div>
    <h3>%s</h3>
    <i>
        <span>行业:%s</span>&nbsp;&nbsp;&nbsp;
        <span>上市时间:%s</span>&nbsp;&nbsp;&nbsp;
        <span>%s</span>&nbsp;&nbsp;&nbsp;
    </i>
</div>
    """ % (stock_basic['name']+' '+stock_basic['symbol'], stock_basic['industry'],
           stock_basic['list_date'], stock_basic['fullname'])
    html = """
<html>
<head>
    <title>%s(%s)财务报表解读</title>
    <meta charset="utf-8">
</head>
<body>
    %s
    <hr/><p></p>
    %s<p></p> %s<p></p> %s<p></p> %s<p></p> %s<p></p> %s
</body>
    """
    table_asset_liability_rate = get_table_html(fina_indicators, '资产负债比率(占总资产%)', asset_liability_rate)
    table_financial_structure = get_table_html(fina_indicators, '财务结构', financial_structure)
    table_solvency = get_table_html(fina_indicators, '偿债能力', solvency)
    table_business_capability = get_table_html(fina_indicators, '经营能力', business_capability)
    table_profitability = get_table_html(fina_indicators, '获利能力', profitability)
    table_cash_flow = get_table_html(fina_indicators, '现金流量', cash_flow)
    return html % (stock_basic['name'], stock_basic['symbol'], stock_basic_html, table_asset_liability_rate,
                   table_financial_structure, table_solvency, table_business_capability, table_profitability,
                   table_cash_flow)
