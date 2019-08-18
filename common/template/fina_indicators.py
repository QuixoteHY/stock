# -*- coding:utf-8 -*-
# @Time     : 2019-06-12 23:21
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : Calculating financial indicators


def get_html_table_code(fina_indicators):
    html = """
<html>
<head>
    <title>财务报表解读</title>
    <meta charset="utf-8">
</head>
<body>
    <table class="fina_indicators" border="8">
        %s
    </table>
</body>
    """
    year_list = ['20'+str(i)+'1231' for i in range(10, 19)]
    table = """<tr style="color:blue;font-weight:bold"><td align=center>财务指标\年份</td>"""
    table = table+'\n'.join(['<td align=center>'+year+'</td>' for year in year_list])+'</tr>'
    header_print = '财务指标\年份'+11*' '+'  '.join(year_list)
    print(header_print)
    for indicator_name, indicators in fina_indicators.items():
        tr_indicator = '<tr><td align=center>'+indicator_name+'</td>'
        temp_string = indicator_name+(20-len(indicator_name)*2)*' '+'\t'
        for year in year_list:
            if year in indicators:
                tr_indicator = tr_indicator+'<td>'+str(indicators[year])+'</td>'
                temp_string = temp_string+str(indicators[year])+(10-len(str(indicators[year])))*' '
            else:
                tr_indicator = tr_indicator + '<td>--</td>'
                temp_string = temp_string + '' + (10 - len('')) * ' '
        tr_indicator += '</tr>'
        table += tr_indicator
        print(temp_string)
    return html % table
