# -*- coding:utf-8 -*-
# @Time     : 2019-06-10 21:37
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :


class Utils(object):
    @staticmethod
    def get_rate(value):
        # 替换内置round函数,实现保留2位小数的精确四舍五入
        # return round(value*100, 1)
        return round(value*1000)/10.0