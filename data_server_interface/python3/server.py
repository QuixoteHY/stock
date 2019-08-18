# -*- coding:utf-8 -*-
# @Time     : 2019-08-18 11:33
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe :

import asyncio

from aiohttp import web

from .logger import logger
from .settings import SERVER_HOST, SERVER_PORT, HEARTBEAT_INTERVAL
from .controller import Controller


def _heartbeat(loop, interval):
    try:
        logger.info('心跳：'+str(interval)+'s')
    except Exception as e:
        logger.info(logger.exception(e))
    loop.call_later(interval, _heartbeat, loop, interval)


def start_heartbeat(loop, interval):
    _heartbeat(loop, interval)


class MainHandler:
    def __init__(self):
        self.controller = Controller()

    async def get_stock_info(self, request):
        remote = request.remote
        logger.info(str(remote))
        try:
            financial_statement_type = request.match_info.get('financial_statement_type', '')
            ts_code = request.match_info.get('ts_code', '')
            if not ts_code:
                return web.json_response({'status': 'no ts_code in your request url'})
            if financial_statement_type == 'balance_sheet':
                self.controller.get_balance_sheet(ts_code)
                return web.json_response({})
            elif financial_statement_type == 'fina_indicators':
                return web.json_response(self.controller.get_fina_indicators(ts_code))
        except Exception as e:
            logger.info(logger.exception(e))
            return web.json_response({'status': 'error in server'})


async def init(loop):
    app = web.Application(loop=loop)
    handler = MainHandler()
    #
    # 获取某上市公司资产负债表信息
    # http://127.0.0.1:8888/get/stock/{financial_statement_type}/{ts_code}
    app.router.add_get('/get/stock/{financial_statement_type}/{ts_code}', handler.get_stock_info)
    #
    # server = await loop.create_server(app.make_handler(), SERVER_HOST, SERVER_PORT)
    # logger.info('\n\tServer started at http://%s:%s...' % (SERVER_HOST, SERVER_PORT))
    # return server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, SERVER_HOST, SERVER_PORT)
    logger.info('\n\tServer started at http://%s:%s...' % (SERVER_HOST, SERVER_PORT))
    await site.start()

if __name__ == '__main__':
    _loop = asyncio.get_event_loop()
    _loop.run_until_complete(init(_loop))
    start_heartbeat(_loop, HEARTBEAT_INTERVAL)
    _loop.run_forever()

