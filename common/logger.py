#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time     : 2019-06-05 16:11
# @Author   : huyuan@zingfront.com
# @description :

import logging

logging.basicConfig(format='[%(asctime)s L:%(lineno)d][%(pathname)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger()
logger.setLevel(logging.INFO)
