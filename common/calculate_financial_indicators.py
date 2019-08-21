# -*- coding:utf-8 -*-
# @Time     : 2019-06-08 22:44
# @Author   : 胡远
# @Github   : https://github.com/QuixoteHY
# @Email    : 1290482442@qq.com
# @Describe : Calculating financial indicators

import copy

from common.constant import data_path
from common.tushare_api import pro
from common.utils import Utils
from common.template.fina_indicators import get_html_table_code
from common.data_model import fina_indicators_dict


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


# def calculate_total_debt_shareholders_equity_rate(balancesheet):
#     # 总资产/负债及股东权益总计*100%
#     total_assets = float(balancesheet['total_assets'] if balancesheet['total_assets'] else 0)
#     total_liab_hldr_eqy = float(balancesheet['total_liab_hldr_eqy'] if balancesheet['total_liab_hldr_eqy'] else 0)
#     if not total_liab_hldr_eqy:
#         return 0
#     return total_assets/total_liab_hldr_eqy


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


def calculate_receivable_turnover_rate(balancesheet, income):
    # 应收账款周转率(次)=营业收入/应收账款*100%
    total_cur_assets = float(income['revenue'] if income['revenue'] else 0)
    accounts_receiv = float(balancesheet['accounts_receiv'] if balancesheet['accounts_receiv'] else 0)
    if not accounts_receiv:
        return 0
    return total_cur_assets/accounts_receiv/100


def calculate_ave_receivable_days(balancesheet, income):
    # 平均收现日数=360/应收账款周转率=360/(营业收入/应收账款*100%)
    total_cur_assets = float(income['revenue'] if income['revenue'] else 0)
    accounts_receiv = float(balancesheet['accounts_receiv'] if balancesheet['accounts_receiv'] else 0)
    if not accounts_receiv:
        return 0
    return 360/((total_cur_assets/accounts_receiv)*100)


def calculate_inventory_turnover(balancesheet, income):
    # 存货周转率(次)=营业成本/存货
    total_cogs = float(income['total_cogs'] if income['total_cogs'] else 0)
    inventories = float(balancesheet['inventories'] if balancesheet['inventories'] else 0)
    if not inventories:
        return 0
    return (total_cogs/inventories)/100


def calculate_ave_sale_days(balancesheet, income):
    # 平均销货日数(平均在库天数)=360/存货周转率
    total_cogs = float(income['total_cogs'] if income['total_cogs'] else 0)
    inventories = float(balancesheet['inventories'] if balancesheet['inventories'] else 0)
    if not inventories:
        return 0
    return 360/((total_cogs/inventories)*100)


def calculate_fixed_invest_turnover_rate(fina_indicator):
    # 固定资产周转率
    fa_turn = float(fina_indicator['fa_turn'] if fina_indicator['fa_turn'] else 0)
    if 'fa_turn' not in fina_indicator:
        return 0
    return float(fa_turn)


def calculate_total_assert_turnover_rate(fina_indicator):
    # 总资产周转率
    assets_turn = float(fina_indicator['assets_turn'] if fina_indicator['assets_turn'] else 0)
    if 'assets_turn' not in fina_indicator:
        return 0
    return float(assets_turn)


def calculate_roe(fina_indicator):
    # 净资产收益率RoE
    roe = float(fina_indicator['roe'] if fina_indicator['roe'] else 0)
    if 'roe' not in fina_indicator:
        return 0
    return float(roe)


def calculate_roa(fina_indicator):
    # 总资产报酬率RoA=归属于母公司所有者的净利润/总资产
    roe = float(fina_indicator['roa'] if fina_indicator['roa'] else 0)
    if 'roa' not in fina_indicator:
        return 0
    return float(roe)


def calculate_operating_margin(fina_indicator):
    # 销售毛利率
    grossprofit_margin = float(fina_indicator['grossprofit_margin'] if fina_indicator['grossprofit_margin'] else 0)
    if 'grossprofit_margin' not in fina_indicator:
        return 0
    return float(grossprofit_margin)


def calculate_business_interest_rate(fina_indicator):
    # 销售净利率
    netprofit_margin = float(fina_indicator['netprofit_margin'] if fina_indicator['netprofit_margin'] else 0)
    if 'netprofit_margin' not in fina_indicator:
        return 0
    return float(netprofit_margin)


def calculate_marginal_rate_of_operational_safety():
    # 经营安全边际率(%) = 营业利益率/营业毛利率
    pass


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


def calculate_eps(fina_indicator):
    # 基本每股收益=每股盈余(元)
    eps = float(fina_indicator['eps'] if fina_indicator['eps'] else 0)
    if 'eps' not in fina_indicator:
        return 0
    return float(eps)


def calculate_n_income(income):
    # 税后净利(百万元)
    n_income = float(income['n_income'] if income['n_income'] else 0)
    return float(n_income)/1000000


def calculate_cash_flow_rate(balancesheet, cash_flow):
    # 现金流量比率=经营活动产生的现金流量净额/流动负债
    n_cashflow_act = float(cash_flow['n_cashflow_act'] if cash_flow['n_cashflow_act'] else 0)
    total_cur_liab = float(balancesheet['total_cur_liab'] if balancesheet['total_cur_liab'] else 0)
    if not total_cur_liab:
        return 0
    return n_cashflow_act/total_cur_liab


def calculate_cash_flow(cash_flow):
    # 营业活动现金流量(百万元)=经营活动产生的现金流量净额
    n_cashflow_act = float(cash_flow['n_cashflow_act'] if cash_flow['n_cashflow_act'] else 0)
    return n_cashflow_act/1000000


def calculate_invest_cash_flow(cash_flow):
    # 投资活动现金流量(百万元)=投资活动产生的现金流量净额
    n_cashflow_inv_act = float(cash_flow['n_cashflow_inv_act'] if cash_flow['n_cashflow_inv_act'] else 0)
    return n_cashflow_inv_act/1000000


def calculate_finance_cash_flow(cash_flow):
    # 筹资活动现金流量(百万元)=筹资活动产生的现金流量净额
    n_cash_flows_fnc_act = float(cash_flow['n_cash_flows_fnc_act'] if cash_flow['n_cash_flows_fnc_act'] else 0)
    return n_cash_flows_fnc_act/1000000


def get_fina_indicator():
    df = pro.fina_indicator(ts_code='000040.SZ', start_date='20050101', end_date='20190630', fields='')
    file = data_path + '/test_data/fina_indicator_000040.SZ'+'.csv'
    df.to_csv(file)


def calculate(ts_code):
    fina_indicators = copy.deepcopy(fina_indicators_dict)
    mongodb_fi = Utils.get_conn_fi()
    stock_info = mongodb_fi.find_one({'_id': ts_code})
    financial_statements = stock_info['financial_statements']
    stock_basic = stock_info['stock_basic']
    for end_date, data in financial_statements.items():
        if not data['balance_sheet'] or not data['income'] or not data['cash_flow'] or not data['fifi']:
            continue
        # 资产负债表
        # 资产负债比率(占总资产%)
        # 现金与约当现金比率
        cash_to_total_assets_rate = calculate_cash_to_total_assets_rate(data['balance_sheet'])
        fina_indicators['现金与约当现金比率'][end_date] = Utils.get_rate(cash_to_total_assets_rate)
        # 应收账款比率
        accounts_receivable_rate = calculate_accounts_receivable_rate(data['balance_sheet'])
        fina_indicators['应收账款比率'][end_date] = Utils.get_rate(accounts_receivable_rate)
        # 存货比率
        inventory_rate = calculate_inventory_rate(data['balance_sheet'])
        fina_indicators['存货比率'][end_date] = Utils.get_rate(inventory_rate)
        # 流动资产比率
        liquidity_rate = calculate_liquidity_rate(data['balance_sheet'])
        fina_indicators['流动资产比率'][end_date] = Utils.get_rate(liquidity_rate)
        # 应付账款比率
        total_accounts_payable_rate = calculate_accounts_payable_rate(data['balance_sheet'])
        fina_indicators['应付账款比率'][end_date] = Utils.get_rate(total_accounts_payable_rate)
        # 流动负债比率
        total_current_liability_rate = calculate_current_liability_rate(data['balance_sheet'])
        fina_indicators['流动负债比率'][end_date] = Utils.get_rate(total_current_liability_rate)
        # 长期负债比率
        total_long_term_debt_rate = calculate_long_term_debt_rate(data['balance_sheet'])
        fina_indicators['长期负债比率'][end_date] = Utils.get_rate(total_long_term_debt_rate)
        # 股东权益比率
        total_shareholder_equity_rate = calculate_shareholder_equity_rate(data['balance_sheet'])
        fina_indicators['股东权益比率'][end_date] = Utils.get_rate(total_shareholder_equity_rate)
        # 五大财务比率
        # 五大财务比率--财务结构
        # 负债占资产比率
        total_debt_to_asset_rate = calculate_debt_to_asset_rate(data['balance_sheet'])
        fina_indicators['负债占资产比率'][end_date] = Utils.get_rate(total_debt_to_asset_rate)
        # 长期资金占不动产/厂房及设备比率 = 长期资金占投资比率
        long_term_capital_to_invest_rate = calculate_long_term_capital_to_invest_rate(data['balance_sheet'])
        fina_indicators['长期资金占投资比率'][end_date] = Utils.get_rate(long_term_capital_to_invest_rate)
        # 五大财务比率--偿债能力
        # 流动比率
        liquidity_asset_to_liquidity_debt_rate = calculate_liquidity_asset_to_liquidity_debt_rate(data['balance_sheet'])
        fina_indicators['流动比率'][end_date] = Utils.get_rate(liquidity_asset_to_liquidity_debt_rate)
        # 速动比率
        quick_moving_rate = calculate_quick_moving_rate(data['balance_sheet'])
        fina_indicators['速动比率'][end_date] = Utils.get_rate(quick_moving_rate)
        # 五大财务比率--经营能力
        # 应收账款周转率(次)
        receivable_turnover_rate = calculate_receivable_turnover_rate(data['balance_sheet'], data['income'])
        fina_indicators['应收账款周转率(次)'][end_date] = Utils.get_rate(receivable_turnover_rate)
        # 平均收现日数
        ave_receive_days = calculate_ave_receivable_days(data['balance_sheet'], data['income'])
        fina_indicators['平均收现日数'][end_date] = Utils.get_rate(ave_receive_days)
        # 存货周转率(次)
        inventory_turnover = calculate_inventory_turnover(data['balance_sheet'], data['income'])
        fina_indicators['存货周转率(次)'][end_date] = Utils.get_rate(inventory_turnover)
        # 平均销货日数(平均在库天数)
        ave_sale_days = calculate_ave_sale_days(data['balance_sheet'], data['income'])
        fina_indicators['平均销货日数(平均在库天数)'][end_date] = Utils.get_rate(ave_sale_days)
        # 固定资产周转率
        fixed_invest_turnover_rate = calculate_fixed_invest_turnover_rate(data['fifi'])
        fina_indicators['固定资产周转率'][end_date] = Utils.get_round(fixed_invest_turnover_rate)
        # 总资产周转率(次)
        total_assert_turnover_rate = calculate_total_assert_turnover_rate(data['fifi'])
        fina_indicators['总资产周转率'][end_date] = Utils.get_round(total_assert_turnover_rate)
        # 五大财务比率--获利能力
        # 净资产收益率RoE
        roe = calculate_roe(data['fifi'])
        fina_indicators['净资产收益率RoE'][end_date] = Utils.get_round(roe)
        # 总资产报酬率RoA
        roa = calculate_roa(data['fifi'])
        fina_indicators['总资产报酬率RoA'][end_date] = Utils.get_round(roa)
        # 销售毛利率
        roe = calculate_operating_margin(data['fifi'])
        fina_indicators['销售毛利率'][end_date] = Utils.get_round(roe)
        # 销售净利率
        roa = calculate_business_interest_rate(data['fifi'])
        fina_indicators['销售净利率'][end_date] = Utils.get_round(roa)
        # 净利率=纯益率
        net_interest_rate = calculate_net_interest_rate(data['income'])
        fina_indicators['净利率'][end_date] = Utils.get_rate(net_interest_rate)
        # 基本每股收益=每股盈余(元)
        surplus_rese_ps = calculate_eps(data['fifi'])
        fina_indicators['基本每股收益'][end_date] = Utils.get_round(surplus_rese_ps)
        # 税后净利(百万元)
        n_income = calculate_n_income(data['income'])
        fina_indicators['税后净利(百万元)'][end_date] = Utils.get_round(n_income)
        # 五大财务比率--现金流量
        # 现金流量比率
        cash_flow_rate = calculate_cash_flow_rate(data['balance_sheet'], data['cash_flow'])
        fina_indicators['现金流量比率'][end_date] = Utils.get_rate(cash_flow_rate)
        # 营业活动现金流量(百万元)
        cash_flow = calculate_cash_flow(data['cash_flow'])
        fina_indicators['营业活动现金流量(百万元)'][end_date] = Utils.get_round(cash_flow)
        # 投资活动现金流量(百万元)
        invest_cash_flow = calculate_invest_cash_flow(data['cash_flow'])
        fina_indicators['投资活动现金流量(百万元)'][end_date] = Utils.get_round(invest_cash_flow)
        # 筹资活动现金流量(百万元)
        finance_cash_flow = calculate_finance_cash_flow(data['cash_flow'])
        fina_indicators['筹资活动现金流量(百万元)'][end_date] = Utils.get_round(finance_cash_flow)
    return get_html_table_code(fina_indicators, stock_basic)


if __name__ == '__main__':
    calculate('002087.SZ')
