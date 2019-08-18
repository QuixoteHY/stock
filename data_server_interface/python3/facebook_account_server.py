# -*- coding:utf-8 -*-
# @Time     : 2018-06-05 11:08
# @Author   : huyuan@zingfront.com
# @Software : SocialPeta
# @description :

import sys
import asyncio
import json

from aiohttp import web

from facebook_account.logger import logger
from facebook_account.settings import FACEBOOK_ACCOUNT_SERVER_HOST, FACEBOOK_ACCOUNT_SERVER_PORT
from facebook_account.settings import BATCH_ACCOUNT_COUNT, BATCH_ACCOUNT_MAX_COUNT, HEARTBEAT_INTERVAL
from facebook_account.facebook_cookies_controller import FacebookCookiesController
from facebook_account.facebook_tokens_controller import FacebookTokensController
from facebook_account.utils import Utils

res = FacebookCookiesController.init_cookies()
if res != 0:
    logger.info('初始化FacebookCookieController出错')
    sys.exit(1)

res = FacebookTokensController.init_tokens()
if res != 0:
    logger.info('初始化FacebookTokensController出错')
    sys.exit(1)


def _heartbeat(loop, interval):
    try:
        date_string = Utils.get_today_string()
        # 更新cookies
        if date_string != FacebookCookiesController.flag_date:
            logger.info('FacebookCookiesController更新flag_date字段：%s > %s' %
                        (FacebookCookiesController.flag_date, date_string))
            FacebookCookiesController.flag_date = date_string
            FacebookCookiesController.reset_status_daily()
        count = FacebookCookiesController.get_all_cookies_use_count()
        logger.info('>>>>> ['+FacebookCookiesController.flag_date+'] all_cookies_use_count: '+str(count))
        count = FacebookCookiesController.get_audience_cookie_count()
        logger.info('>>>>> ['+FacebookCookiesController.flag_date+'] audience_cookie_count: '+str(count))
        # 更新tokens
        if date_string != FacebookTokensController.flag_date:
            logger.info('FacebookTokensController更新flag_date字段：%s > %s' %
                        (FacebookTokensController.flag_date, date_string))
            FacebookTokensController.flag_date = date_string
            FacebookTokensController.reset_status_daily()
        count = FacebookTokensController.get_all_tokens_use_count()
        logger.info('>>>>> ['+FacebookTokensController.flag_date+'] all_tokens_use_count: '+str(count))
    except Exception as e:
        logger.info(logger.exception(e))
    loop.call_later(interval, _heartbeat, loop, interval)


def start_heartbeat(loop, interval):
    _heartbeat(loop, interval)


class FacebookAccountHandler:
    def __init__(self):
        pass

    @staticmethod
    def err_msg(err_code):
        return {'error': {'code': err_code, 'message': 'None'}}

    @staticmethod
    def new_account_model():
        return {'status': 0, 'account_type': '', 'account_id': '', 'account_str': '',
                'fb_dtsg_ag': '', 'admarket_id': '', 'note': ''}

    @staticmethod
    def new_batch_accounts_model():
        """
        accounts:
            if cookies: [{'account_id': '', 'account_str': ''}, {'account_id': '', 'account_str': ''}, ...]
            if audience_cookies: [{'account_id': '', 'account_str': '', 'fb_dtsg_ag': '', 'admarket_id': ''}, ...]
            if tokens: [{'account_id': '', 'account_str': ''}, {'account_id': '', 'account_str': ''}, ...]
        :return:
        """
        return {'status': 0, 'account_type': '', 'accounts': list(), 'note': ''}

    @staticmethod
    def new_status_model():
        return {'status': 0, 'result': '', 'note': ''}

    async def get_account(self, request):
        data = self.new_account_model()
        remote = request.remote
        params = self._parse_qs(request.query_string)
        params['remote'] = remote
        if not params.get('func_type'):
            data = FacebookAccountHandler.err_msg(400)
            return web.json_response(data)
        try:
            account_type = request.match_info.get('account_type', 'None')
            data['account_type'] = account_type
            arg_account_id = request.match_info.get('account_id', None)
            if arg_account_id is None:
                account_id = None
            else:
                try:
                    account_id = int(arg_account_id)
                except Exception as e:
                    data = self.err_msg(400)
                    data['error']['message'] = 'account_id can\'t to int, account_id='+str(arg_account_id)
                    logger.info(logger.exception(e))
                    return web.json_response(data)
            fb_dtsg_ag, admarket_id = '', ''
            if account_type == 'cookie':
                account_id, account_str = FacebookCookiesController.get_cookie(cookie_id=account_id, **params)
            elif account_type == 'audience_cookie':
                account_id, account_str, fb_dtsg_ag, admarket_id = \
                    FacebookCookiesController.get_audience_cookie(cookie_id=account_id, **params)
            elif account_type == 'token':
                account_id, account_str = FacebookTokensController.get_token(token_id=account_id, **params)
            else:
                data['status'] = 3
                data['note'] = data['note'] + 'account_type is wrong, account_type='+account_type
                logger.info('account_type is wrong, account_type='+account_type)
                return web.json_response(data)
            if account_str is not None:
                data['account_id'] = account_id
                data['account_str'] = account_str
                data['fb_dtsg_ag'] = fb_dtsg_ag
                data['admarket_id'] = admarket_id
                return web.json_response(data)
            else:
                data['status'] = 2
                data['note'] = 'No account, account_id='+str(arg_account_id)
                return web.json_response(data)
        except Exception as e:
            data = self.err_msg(500)
            data['error']['message'] = 'Error in server, '+str(e)
            logger.info(logger.exception(e))
            return web.json_response(data)

    async def get_batch_accounts(self, request):
        data = self.new_batch_accounts_model()
        remote = request.remote
        params = self._parse_qs(request.query_string)
        params['remote'] = remote

        if not params.get('func_type'):
            data = FacebookAccountHandler.err_msg(400)
            return web.json_response(data)

        try:
            account_type = request.match_info.get('account_type', 'None')
            data['account_type'] = account_type
            arg_number = request.match_info.get('number', None)
            if arg_number is None:
                number = BATCH_ACCOUNT_COUNT
            else:
                try:
                    number = int(arg_number)
                except Exception as e:
                    data = self.err_msg(400)
                    data['error']['message'] = 'number can\'t to int, number='+str(arg_number)
                    logger.info(logger.exception(e))
                    return web.json_response(data)
            if number > BATCH_ACCOUNT_MAX_COUNT:
                number = BATCH_ACCOUNT_MAX_COUNT
                data['note'] = 'The number of accounts you require exceeds '+str(BATCH_ACCOUNT_MAX_COUNT) + \
                               ', so I just give you '+str(BATCH_ACCOUNT_MAX_COUNT)+'.'
            if account_type == 'cookie':
                cookie_list = FacebookCookiesController.get_batch_cookies(number, **params)
            elif account_type == 'audience_cookie':
                cookie_list = FacebookCookiesController.get_batch_audience_cookies(number, **params)
            elif account_type == 'token':
                cookie_list = FacebookTokensController.get_batch_tokens(number, **params)
            else:
                data['status'] = 3
                data['note'] = data['note'] + 'account_type is wrong, account_type='+account_type
                logger.info('account_type is wrong, account_type='+account_type)
                return web.json_response(data)
            if len(cookie_list) == number:
                data['accounts'] = cookie_list
                data['note'] = data['note']+'Accounts length = '+str(len(cookie_list))
                return web.json_response(data)
            else:
                data['status'] = 2
                data['accounts'] = cookie_list
                data['note'] = data['note']+'Accounts length = '+str(len(cookie_list))
                return web.json_response(data)
        except Exception as e:
            data = self.err_msg(500)
            data['error']['message'] = 'Error in server, '+str(e)
            logger.info(logger.exception(e))
            return web.json_response(data)

    async def search_accounts(self, request):
        data = self.new_batch_accounts_model()
        remote = request.remote
        params = self._parse_qs(request.query_string)
        params['remote'] = remote
        try:
            account_type = request.match_info.get('account_type', 'None')
            data['account_type'] = account_type
            arg_start_id = request.match_info.get('start_id', None)
            arg_number = request.match_info.get('number', None)
            if arg_start_id is None:
                start_id = 0
            else:
                try:
                    start_id = int(arg_start_id)
                except Exception as e:
                    data = self.err_msg(400)
                    data['error']['message'] = 'start_id can\'t to int, start_id='+str(arg_start_id)
                    logger.info(logger.exception(e))
                    return web.json_response(data)
            if arg_number is None:
                number = BATCH_ACCOUNT_COUNT
            else:
                try:
                    number = int(arg_number)
                except Exception as e:
                    data = self.err_msg(400)
                    data['error']['message'] = 'number can\'t to int, number='+str(arg_number)
                    logger.info(logger.exception(e))
                    return web.json_response(data)
            if number > BATCH_ACCOUNT_MAX_COUNT:
                number = BATCH_ACCOUNT_MAX_COUNT
                data['note'] = 'The number of accounts you require exceeds '+str(BATCH_ACCOUNT_MAX_COUNT) + \
                               ', so I just give you '+str(BATCH_ACCOUNT_MAX_COUNT)+'.'
            if account_type == 'token':
                cookie_list = FacebookTokensController.search_tokens(start_id, number, **params)
            else:
                data['status'] = 3
                data['note'] = data['note'] + 'account_type is wrong, account_type='+account_type
                logger.info('account_type is wrong, account_type='+account_type)
                return web.json_response(data)
            data['accounts'] = cookie_list
            data['note'] = data['note']+'Accounts length = '+str(len(cookie_list))
            return web.json_response(data)
        except Exception as e:
            data = self.err_msg(500)
            data['error']['message'] = 'Error in server, +'+str(e)
            logger.info(logger.exception(e))
            return web.json_response(data)

    async def get_status(self, request):
        data = self.new_status_model()
        try:
            arg_account_type = request.match_info.get('account_type', '')
            arg_operation_type = request.match_info.get('operation_type', '')
            if arg_operation_type == 'count':
                if arg_account_type == 'cookie':
                    count = FacebookCookiesController.get_cookie_count()
                elif arg_account_type == 'token':
                    count = FacebookTokensController.get_tokens_count()
                elif arg_account_type == 'audience_cookie':
                    count = FacebookCookiesController.get_audience_cookie_count()
                else:
                    data['status'] = 2
                    data['note'] = 'I can\'t recognize your instructions, account_type=' + str(arg_account_type)
                    return web.json_response(data)
                data['result'] = json.dumps(count)
                return web.json_response(data)
            elif arg_operation_type == 'account_use_info':
                arg_account_id = request.match_info.get('account_id', None)
                try:
                    account_id = int(arg_account_id)
                except Exception as e:
                    data = self.err_msg(400)
                    data['error']['message'] = 'account_id can\'t to int, account_id='+str(arg_account_id)
                    logger.info(e)
                    return web.json_response(data)
                if arg_account_type == 'cookie':
                    count = FacebookCookiesController.get_the_cookie_use_info(account_id)
                elif arg_account_type == 'token':
                    count = FacebookTokensController.get_the_token_use_info(account_id)
                else:
                    data['status'] = 2
                    data['note'] = 'I can\'t recognize your instructions, account_type=' + str(arg_account_type)
                    return web.json_response(data)
                data['result'] = json.dumps(count)
                return web.json_response(data)
            elif arg_operation_type == 'all':
                if arg_account_type == 'cookie':
                    result = FacebookCookiesController.get_all_cookie_using_status()
                    data['result'] = json.dumps(result)
                    return web.json_response(data)
                elif arg_account_type == 'token':
                    result = FacebookTokensController.get_all_token_using_status()
                    data['result'] = json.dumps(result)
                    return web.json_response(data)
            else:
                data['status'] = 2
                data['note'] = 'I can\'t recognize your instructions, operation_type='+str(arg_operation_type)
                return web.json_response(data)
        except Exception as e:
            data = self.err_msg(500)
            data['error']['message'] = 'Error in server, '+str(e)
            logger.info(logger.exception(e))
            return web.json_response(data)

    def _parse_qs(self, query_string) -> dict:
        params = dict()
        if not query_string:
            return params
        try:
            for query in query_string.split('&'):
                k_v = query.split('=')
                params[k_v[0]] = k_v[1]
            return params
        except Exception as e:
            logger.error(e)
            return params


async def init(loop):
    app = web.Application(loop=loop)
    handler = FacebookAccountHandler()
    #
    # 获取单个cookie、token
    # http://127.0.0.1:8080/cookie/get
    # http://192.168.3.13:8080/audience_cookie/get
    app.router.add_get('/{account_type}/get', handler.get_account)
    # http://192.168.3.13:8080/cookie/id/185247
    # http://127.0.0.1:8080/audience_cookie/id/185247
    app.router.add_get('/{account_type}/id/{account_id}', handler.get_account)
    #
    # 随机批量获取cookie、token
    # http://127.0.0.1:8080/cookie/batch
    app.router.add_get('/{account_type}/batch', handler.get_batch_accounts)
    # http://127.0.0.1:8080/cookie/batch/{number}
    app.router.add_get('/{account_type}/batch/{number}', handler.get_batch_accounts)

    # 顺序批量获取cookie、token
    # http://127.0.0.1:8080/token/search/0
    app.router.add_get('/{account_type}/search/{start_id}', handler.search_accounts)
    # http://127.0.0.1:8080/token/search/0/10
    app.router.add_get('/{account_type}/search/{start_id}/{number}', handler.search_accounts)
    # cookie、token状态
    # http://192.168.3.13:8080/status/cookie/count
    # http://127.0.0.1:8080/status/audience_cookie/count
    app.router.add_get('/status/{account_type}/{operation_type}', handler.get_status)
    # http://127.0.0.1:8080/status/cookie/account_use_info/185247
    app.router.add_get('/status/{account_type}/{operation_type}/{account_id}', handler.get_status)
    # http://127.0.0.1:8080/status/cookie/all
    # http://127.0.0.1:8080/status/token/all
    app.router.add_get('/status/{account_type}/{operation_type}', handler.get_status)
    #
    # server = await loop.create_server(app.make_handler(), FACEBOOK_COOKIE_SERVER_HOST, FACEBOOK_COOKIE_SERVER_PORT)
    # logger.info('\n\tServer started at http://%s:%s...' % (FACEBOOK_COOKIE_SERVER_HOST, FACEBOOK_COOKIE_SERVER_PORT))
    # return server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, FACEBOOK_ACCOUNT_SERVER_HOST, FACEBOOK_ACCOUNT_SERVER_PORT)
    logger.info('\n\tServer started at http://%s:%s...' % (FACEBOOK_ACCOUNT_SERVER_HOST, FACEBOOK_ACCOUNT_SERVER_PORT))
    await site.start()

if __name__ == '__main__':
    _loop = asyncio.get_event_loop()
    _loop.run_until_complete(init(_loop))
    start_heartbeat(_loop, HEARTBEAT_INTERVAL)
    _loop.run_forever()
