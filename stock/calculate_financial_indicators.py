# -*- coding:utf-8 -*-
# @Time     : 2019-06-08 22:44
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : Calculating financial indicators

import logging
import copy
import csv

from settings import data_path, pro
from stock.utils import Utils
from stock.template.fina_indicators import get_table_code
from stock import fina_indicators_dict


def calculate_cash_to_total_assets_rate(balancesheet):
    # 现金与约当现金比率=现金占总资产比率=(货币资金+交易性金融资产)/总资产*100%
    money_cap = float(balancesheet['money_cap'] if balancesheet['money_cap'] else 0)
    trad_asset = float(balancesheet['trad_asset'] if balancesheet['trad_asset'] else 0)
    total_assets = float(balancesheet['total_assets'] if balancesheet['total_assets'] else 0)
    if not total_assets:
        return 0
    return (money_cap+trad_asset)/total_assets


def calculate_accounts_receivable_rate(balancesheet):
    # 应收账款比率=应收账款/总资产*100%
    accounts_receiv = float(balancesheet['accounts_receiv'] if balancesheet['accounts_receiv'] else 0)
    total_assets = float(balancesheet['total_assets'] if balancesheet['total_assets'] else 0)
    if not total_assets:
        return 0
    return accounts_receiv/total_assets


def calculate_inventory_rate(balancesheet):
    # 存货比率=存货/总资产*100%
    inventories = float(balancesheet['inventories'] if balancesheet['inventories'] else 0)
    total_assets = float(balancesheet['total_assets'] if balancesheet['total_assets'] else 0)
    if not total_assets:
        return 0
    return inventories/total_assets


def calculate_liquidity_rate(balancesheet):
    # 流动资产比率=流动资产合计/总资产*100%
    total_cur_assets = float(balancesheet['total_cur_assets'] if balancesheet['total_cur_assets'] else 0)
    total_assets = float(balancesheet['total_assets'] if balancesheet['total_assets'] else 0)
    if not total_assets:
        return 0
    return total_cur_assets/total_assets


def calculate_accounts_payable_rate(balancesheet):
    # 应付账款比率=应付账款/总资产*100%
    acct_payable = float(balancesheet['acct_payable'] if balancesheet['acct_payable'] else 0)
    total_assets = float(balancesheet['total_assets'] if balancesheet['total_assets'] else 0)
    if not total_assets:
        return 0
    return acct_payable/total_assets


def calculate_current_liability_rate(balancesheet):
    # 流动负债比率=流动负债合计/总资产*100%
    total_cur_liab = float(balancesheet['total_cur_liab'] if balancesheet['total_cur_liab'] else 0)
    total_assets = float(balancesheet['total_assets'] if balancesheet['total_assets'] else 0)
    if not total_assets:
        return 0
    return total_cur_liab/total_assets


def calculate_long_term_debt_rate(balancesheet):
    # 长期负债比率=非流动负债/总资产*100%
    total_ncl = float(balancesheet['total_ncl'] if balancesheet['total_ncl'] else 0)
    total_assets = float(balancesheet['total_assets'] if balancesheet['total_assets'] else 0)
    if not total_assets:
        return 0
    return total_ncl/total_assets


def calculate_shareholder_equity_rate(balancesheet):
    # 股东权益比率=股东权益合计(含少数股东权益)/总资产*100%
    total_hldr_eqy_inc_min_int = \
        float(balancesheet['total_hldr_eqy_inc_min_int'] if balancesheet['total_hldr_eqy_inc_min_int'] else 0)
    total_assets = float(balancesheet['total_assets'] if balancesheet['total_assets'] else 0)
    if not total_assets:
        return 0
    return total_hldr_eqy_inc_min_int/total_assets


def calculate_total_debt_shareholders_equity_rate(balancesheet):
    # 总资产/负债及股东权益总计*100%
    total_assets = float(balancesheet['total_assets'] if balancesheet['total_assets'] else 0)
    total_liab_hldr_eqy = float(balancesheet['total_liab_hldr_eqy'] if balancesheet['total_liab_hldr_eqy'] else 0)
    if not total_liab_hldr_eqy:
        return 0
    return total_assets/total_liab_hldr_eqy


def calculate_debt_to_asset_rate(balancesheet):
    # 负债占资产比率=总负债/总资产*100%
    total_liab = float(balancesheet['total_liab'] if balancesheet['total_liab'] else 0)
    total_assets = float(balancesheet['total_assets'] if balancesheet['total_assets'] else 0)
    if not total_assets:
        return 0
    return total_liab/total_assets


def calculate_long_term_capital_to_invest_rate(balancesheet):
    # 长期资金占不动产/厂房及设备比率=长期资金占投资比率=(长期负债+股东权益)/(固定资产+在建工程+工程物资)(不动产、厂房及设备)*100%
    # 长期资金占不动产、厂房及设备比率=（所有者权益（或股东权益）合计 + 非流动负债合计） / ( 固定资产 + 在建工程 + 工程物资)
    total_ncl = float(balancesheet['total_ncl'] if balancesheet['total_ncl'] else 0)
    total_hldr_eqy_inc_min_int = \
        float(balancesheet['total_hldr_eqy_inc_min_int'] if balancesheet['total_hldr_eqy_inc_min_int'] else 0)
    fix_assets = float(balancesheet['fix_assets'] if balancesheet['fix_assets'] else 0)
    cip = float(balancesheet['cip'] if balancesheet['cip'] else 0)
    const_materials = float(balancesheet['const_materials'] if balancesheet['const_materials'] else 0)
    if fix_assets+cip+const_materials:
        return (total_ncl+total_hldr_eqy_inc_min_int)/(fix_assets+cip+const_materials)
    else:
        return total_ncl+total_hldr_eqy_inc_min_int


def calculate_liquidity_asset_to_liquidity_debt_rate(balancesheet):
    # 流动比率=流动资产/流动负债*100%
    total_cur_assets = float(balancesheet['total_cur_assets'] if balancesheet['total_cur_assets'] else 0)
    total_cur_liab = float(balancesheet['total_cur_liab'] if balancesheet['total_cur_liab'] else 0)
    if not total_cur_liab:
        return 0
    return total_cur_assets/total_cur_liab


def calculate_quick_moving_rate(balancesheet):
    # 速动比率=（流动资产-存货)/流动负债*100%
    # 速动资产=流动资产-存货，或：速动资产=流动资产-存货-预付账款-待摊费用
    total_cur_assets = float(balancesheet['total_cur_assets'] if balancesheet['total_cur_assets'] else 0)
    inventories = float(balancesheet['inventories'] if balancesheet['inventories'] else 0)
    prepayment = float(balancesheet['prepayment'] if balancesheet['prepayment'] else 0)
    amor_exp = float(balancesheet['amor_exp'] if balancesheet['amor_exp'] else 0)
    total_cur_liab = float(balancesheet['total_cur_liab'] if balancesheet['total_cur_liab'] else 0)
    if not total_cur_liab:
        return 0
    return (total_cur_assets-inventories-prepayment-amor_exp)/total_cur_liab


def calculate_receivable_turnover_rate(balancesheet):
    # 应收账款周转率=营业收入/应收账款*100%
    total_cur_assets = float(balancesheet['total_cur_assets'] if balancesheet['total_cur_assets'] else 0)
    total_cur_liab = float(balancesheet['total_cur_liab'] if balancesheet['total_cur_liab'] else 0)
    if not total_cur_liab:
        return 0
    return total_cur_assets/total_cur_liab


def calculate_net_interest_rate(income):
    # 净利率=净利润/主营业务收入×100%=(利润总额-所得税费用)/主营业务收入*100%
    total_profit = income['total_profit'].strip()
    if not total_profit:
        total_profit = 0
    total_profit = float(total_profit)
    income_tax = income['income_tax'].strip()
    if not income_tax:
        income_tax = 0
    income_tax = float(income_tax)
    revenue = income['revenue'].strip()
    if not revenue:
        revenue = 0
    revenue = float(revenue)
    if not revenue:
        return 0
    return (total_profit-income_tax)/revenue


def get_fina_indicator():
    df = pro.fina_indicator(ts_code='000040.SZ', start_date='20050101', end_date='20190630', fields='')
    file = data_path + '/test_data/fina_indicator_000040.SZ'+'.csv'
    df.to_csv(file)


def calculate(ts_code, conn_collection):
    fina_indicators = copy.deepcopy(fina_indicators_dict)
    bs_file = data_path + '/balancesheet/balancesheet_20190630_%s.csv' % ts_code
    ic_file = data_path + '/income/income_20190630_%s.csv' % ts_code
    with open(bs_file, newline='', encoding='UTF-8') as bsf:
        # 资产负债表
        bs_reader = csv.DictReader(bsf)
        for row in bs_reader:
            # 资产负债比率(占总资产%)
            # 现金与约当现金比率
            cash_to_total_assets_rate = calculate_cash_to_total_assets_rate(row)
            fina_indicators['现金与约当现金比率'][row['end_date']] = Utils.get_rate(cash_to_total_assets_rate)
            # 应收账款比率
            accounts_receivable_rate = calculate_accounts_receivable_rate(row)
            fina_indicators['应收账款比率'][row['end_date']] = Utils.get_rate(accounts_receivable_rate)
            # 存货比率
            inventory_rate = calculate_inventory_rate(row)
            fina_indicators['存货比率'][row['end_date']] = Utils.get_rate(inventory_rate)
            # 流动资产比率
            liquidity_rate = calculate_liquidity_rate(row)
            fina_indicators['流动资产比率'][row['end_date']] = Utils.get_rate(liquidity_rate)
            # 应付账款比率
            total_accounts_payable_rate = calculate_accounts_payable_rate(row)
            fina_indicators['应付账款比率'][row['end_date']] = Utils.get_rate(total_accounts_payable_rate)
            # 流动负债比率
            total_current_liability_rate = calculate_current_liability_rate(row)
            fina_indicators['流动负债比率'][row['end_date']] = Utils.get_rate(total_current_liability_rate)
            # 长期负债比率
            total_long_term_debt_rate = calculate_long_term_debt_rate(row)
            fina_indicators['长期负债比率'][row['end_date']] = Utils.get_rate(total_long_term_debt_rate)
            # 股东权益比率
            total_shareholder_equity_rate = calculate_shareholder_equity_rate(row)
            fina_indicators['股东权益比率'][row['end_date']] = Utils.get_rate(total_shareholder_equity_rate)
            # 资产负债表平衡
            total_debt_shareholders_equity_rate = calculate_total_debt_shareholders_equity_rate(row)
            fina_indicators['资产负债表平衡'][row['end_date']] = \
                Utils.get_rate(total_debt_shareholders_equity_rate)
            # 五大财务比率
            # 五大财务比率--财务结构
            # 负债占资产比率
            total_debt_to_asset_rate = calculate_debt_to_asset_rate(row)
            fina_indicators['负债占资产比率'][row['end_date']] = Utils.get_rate(total_debt_to_asset_rate)
            # 长期资金占不动产/厂房及设备比率 = 长期资金占投资比率
            long_term_capital_to_invest_rate = calculate_long_term_capital_to_invest_rate(row)
            fina_indicators['长期资金占投资比率'][row['end_date']] = Utils.get_rate(long_term_capital_to_invest_rate)
            # 五大财务比率--偿债能力
            # 流动比率
            liquidity_asset_to_liquidity_debt_rate = calculate_liquidity_asset_to_liquidity_debt_rate(row)
            fina_indicators['流动比率'][row['end_date']] = Utils.get_rate(liquidity_asset_to_liquidity_debt_rate)
            # 速动比率
            quick_moving_rate = calculate_quick_moving_rate(row)
            fina_indicators['速动比率'][row['end_date']] = Utils.get_rate(quick_moving_rate)
            # 五大财务比率--经营能力
            # 应收账款周转率
            # receivable_turnover_rate = calculate_receivable_turnover_rate(row, row)
            # fina_indicators['应收账款周转率'][row['end_date']] = Utils.get_rate(receivable_turnover_rate)
    with open(ic_file, newline='', encoding='UTF-8') as icf:
        # 现金流量表
        ic_reader = csv.DictReader(icf)
        for row in ic_reader:
            # 净利率
            net_interest_rate = calculate_net_interest_rate(row)
            fina_indicators['净利率'][row['end_date']] = Utils.get_rate(net_interest_rate)
    get_table_code(fina_indicators)
    conn_collection.insert({ts_code.replace('.', '_'): fina_indicators})


def run():
    conn_collection = Utils.get_conn_fi()
    date_str = '20190608'
    file = data_path + '/stock_basic/all_stock_list_' + date_str + '.csv'
    count = 0
    with open(file, newline='', encoding='UTF-8') as cf:
        reader = csv.DictReader(cf)
        for row in reader:
            count += 1
            try:
                calculate(str(row['ts_code']), conn_collection)
                print(str(count) + '\t', row['ts_code'], row['fullname'], '\t\t\t\t\t\t财务指标计算成功')
            except Exception as e:
                logging.info(logging.exception(e))
                print(str(count) + '\t', row['ts_code'], '\t\t财务指标计算失败')


if __name__ == '__main__':
    run()
