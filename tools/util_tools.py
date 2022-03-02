

import os
import talib as ta
import pandas as pd
import orjson
from datetime import datetime, timedelta

from si_utils.config import base_config as con
from si_utils.config.data_structure import cache_name_dict
from si_utils.tools import cache


# from ff_utils.tools import util_tools as ut
from ff_utils.tools import util_tools as ff_ut
from ff_utils.data_accessing import data_api
from ff_utils.data_accessing.db import PGEngine, table_name_dict
from ff_utils.tools.logger import LogHelper
logger = LogHelper().logger


# region datetime
date_format = '%Y-%m-%d'

def get_ak_td_array(end_date=ff_ut.get_today_str()):
    td_df=PGEngine.table2df(table_name_dict['dc_ak_trade_date'])
    td_array = td_df['trade_date']
    return td_array[td_array<=end_date]

def get_all_days(start_date=None, end_date=None):
    def gen_dates(_b_date, _days):
        _day = timedelta(days=1)
        for _i in range(_days+1):
            yield _b_date + _day*_i
    if start_date is None:
        start_date = datetime.strptime('1999-01-01', date_format)
    if end_date is None:
        end_date = datetime.today()
    else:
        end_date = datetime.strptime(end_date, date_format)
    all_days = []
    for d in gen_dates(start_date, (end_date-start_date).days):
        all_days.append(d)
    return list(map(lambda x:x.strftime(date_format), all_days))

def get_ak_no_trade_days(start_date=None, end_date=ff_ut.get_today_str()):
    trade_day_array = pd.to_datetime(get_ak_td_array(end_date).values)
    trade_day_list = list(map(lambda x:x.strftime(date_format), trade_day_array))
    if start_date is None:
        start_date = trade_day_array[0]
    all_day_list = get_all_days(start_date=start_date, end_date=end_date)
    r_list = list(set(all_day_list).difference(set(trade_day_list))) # all_days中有而trade_days中没有的
    r_list.sort()
    return all_day_list[-1], trade_day_list[-1], r_list

# endregion datetime


# region dpp_s
def grouped_s_code(s_code_list=None, prefix_n=4):
    if s_code_list is None:
        s_code_list = list(get_cached_ak_s_df_realtime()['代码'].values)
    s_code_dict = {}
    for s_code in s_code_list:
        pn = s_code[:prefix_n]
        if pn not in s_code_dict:
            s_code_dict[pn] = []
        s_code_dict[pn].append(s_code)
    return s_code_dict

def get_ak_s_pa_daily_from_DB(s_code_list=None, column_list=None, slicing_window=-1):
    if column_list is None:
        column_list = ['td','s_code', 'turnover_rate', 'v', 'a', 'o', 'c', 'h', 'l', 'o_qfq', 'c_qfq', 'h_qfq', 'l_qfq', 'o_hfq', 'c_hfq', 'h_hfq', 'l_hfq']
    con_td = "'td'>'{0}'".format(ff_ut.get_date_before(ff_ut.get_today_str(), slicing_window)) if slicing_window>0 else None
    con_s_code = None if s_code_list is None else "s_code in ({0})".format(','.join(list(map(lambda x:"'{0}'".format(x), s_code_list))))
    where_con = None
    if con_td is None and con_s_code is None:
        where_con = ";"
    elif con_td is not None and con_s_code is not None:
        where_con = " where {0} and {1};".format(con_td, con_s_code)
    elif con_td is None and con_s_code is not None:
        where_con = " where {0};".format(con_s_code)
    else:
        where_con = " where {0};".format(con_td)
    select_s_daily_sql = """select {0} from "{1}"{2}""".format(','.join(column_list), table_name_dict['dc_ak_a_stock_hist_daily'], where_con)
    td_df = None
    with PGEngine.db_engine.connect() as conn:
        td_df = pd.DataFrame(conn.execute(select_s_daily_sql).fetchall(), columns=column_list)
        logger.info('get {0} data from table {1}'.format(len(td_df), table_name_dict['dc_ak_a_stock_hist_daily']))
    return td_df

def get_pa_columnar_df(row_pa_df, col_name):
    columnar_df_list = []
    for s_code, g_df in row_pa_df.groupby('s_code'):
        _df = g_df.set_index('td')
        if len(_df) < 1:
            continue
        columnar_df_list.append(_df[[col_name]].rename(columns={col_name:s_code}))
    if len(columnar_df_list) < 1:
        logger.info('row pa df is empty.')
        return pd.DataFrame({'td':[]}).set_index('td')
    r_df = pd.concat(columnar_df_list, axis=1)
    r_df.sort_index(inplace=True)
    logger.info('get {0} columnar df of {1}'.format(len(r_df), col_name))
    return r_df

def update_ak_pa_col_file(s_code_pre, col_name):
    col_file_name = os.path.join(con.ak_col_data_file_root, '{0}@{1}.csv'.format(col_name, s_code_pre))
    row_df = get_ak_s_pa_daily_from_DB(grouped_s_code()[s_code_pre], ['s_code', 'td', col_name])
    r_col_df = get_pa_columnar_df(row_df, col_name)
    if len(r_col_df) > 1:
        r_col_df.to_csv(col_file_name, index=True)
        logger.info('save {0} columnar df to file {1}'.format(len(r_col_df), col_file_name))
    return r_col_df

def get_last_valid_td(hour_f=15.5):
    td_array = data_api.get_trade_day_array()
    hour_now = datetime.now().hour
    minute_now = datetime.now().minute
    logger.debug('hour_f={0}, hour_now={1}, minute_now={2}'.format(hour_f, hour_now, minute_now))
    col1 = hour_now > int(hour_f)
    col2 = hour_now == int(hour_f) and minute_now > int((hour_f - int(hour_f))*60)
    if col1 or col2:
        return td_array[-1]
    else:
        return td_array[-2]

def get_ak_pa_col_df(col_name, s_code_list=None):
    s_code_dict = grouped_s_code(s_code_list)
    r_df_list = []
    for s_code_pre, s_code_list in s_code_dict.items():
        col_file_name = os.path.join(con.ak_col_data_file_root, '{0}@{1}.csv'.format(col_name, s_code_pre))
        r_col_df = None
        missing_list = None
        if os.path.exists(col_file_name):
            r_col_df = pd.read_csv(col_file_name)
            logger.debug('get {0} columnar df from file {1}'.format(len(r_col_df), col_file_name))
            r_col_df.set_index('td', inplace=True)
            missing_list = ff_ut.list_diff(s_code_list, r_col_df.columns)
            exist_list = ff_ut.list_diff(s_code_list, missing_list)
            last_valid_td = get_last_valid_td()
            logger.debug('last_valid_td = {0}'.format(last_valid_td))
            con1 = len(missing_list) > 0
            logger.debug(r_col_df[exist_list])
            logger.debug(r_col_df[exist_list].loc[[last_valid_td]])
            logger.debug(r_col_df[exist_list].loc[[last_valid_td]].isna())
            logger.debug(r_col_df[exist_list].loc[[last_valid_td]].isna().any(axis=1))
            con2 = last_valid_td in r_col_df.index and r_col_df[exist_list].loc[[last_valid_td]].isna().any(axis=1)
            if  con1 or con2:
                logger.warning('missing {0} col data in file {1}.'.format(missing_list, col_file_name))
                r_col_df = update_ak_pa_col_file(s_code_pre, col_name)
        else:
            r_col_df = update_ak_pa_col_file(s_code_pre, col_name)
            missing_list = ff_ut.list_diff(s_code_list, r_col_df.columns)
            if len(missing_list) > 0:
                logger.warning('missing {0} col data in row table.'.format(missing_list))
        exist_list = ff_ut.list_diff(s_code_list, missing_list)
        if len(missing_list) < 1 and r_col_df is not None and len(r_col_df[exist_list]) > 0:
            r_df_list.append(r_col_df[exist_list])
            continue
        # 文件不存在或者csv文件中缺少s_code
        # if r_col_df is not None and len(r_col_df[s_code_list]) > 0:
        #     r_df_list.append(r_col_df[s_code_list])
    if len(r_df_list) > 0:
        return pd.concat(r_df_list, axis=1).dropna(how='all')
    else:
        return None

def get_cached_ak_s_df_realtime():
    rt_df_json = cache.dc_cache_get_value(cache_name_dict['dc_ak_s_daily_realtime'])
    if rt_df_json is not None:
        return pd.DataFrame(orjson.loads(rt_df_json))
    else:
        return None

def get_cached_ak_s_dwm(period='daily'):
    ak_daily_keys = [x for x in cache.dc_cache.keys() if x.startswith('dc_ak@') and x.endswith('@'+period)]
    ak_daily_values = list(map(lambda x:orjson.loads(orjson.loads(cache.dc_cache_get_value(x))['data_value']), ak_daily_keys))
    ak_daily_df = pd.DataFrame(ak_daily_values)
    return ak_daily_df

def get_ak_s_realtime():
    cache.dc_cache_get_value(cache_name_dict['dc_ak_s_daily_realtime'])
# endregion dpp_s

# region indicators
def sctr(input_array, sctr_params=con.sctr_params):
    def _n(_array):
        return (_array-min(_array))/(max(_array)-min(_array))
    l_ema = _n(ta.EMA(input_array, timeperiod=sctr_params['l_ema_param']).dropna())
    l_roc = _n(ta.ROC(input_array, timeperiod=sctr_params['l_roc_param']).dropna())
    m_ema = _n(ta.EMA(input_array, timeperiod=sctr_params['m_ema_param']).dropna())
    m_roc = _n(ta.ROC(input_array, timeperiod=sctr_params['m_roc_param']).dropna())
    s_ppo = ta.PPO(input_array, fastperiod=sctr_params['s_ppo_param'][0], slowperiod=sctr_params['s_ppo_param'][1]).dropna()
    s_ppo_h = _n((s_ppo - ta.EMA(s_ppo, timeperiod=sctr_params['s_ppo_param'][2])).dropna())
    s_rsi = _n(ta.RSI(input_array, timeperiod=sctr_params['s_rsi_param']).dropna())
    sctr_array = l_ema * sctr_params['l_ema_ratio'] + l_roc * sctr_params['l_roc_ratio'] + \
                m_ema * sctr_params['m_ema_ratio'] + m_roc * sctr_params['m_roc_ratio'] + \
                s_ppo_h * sctr_params['s_ppo_ratio'] + s_rsi * sctr_params['s_rsi_ratio']
    sctr_array = sctr_array.dropna()
    return sctr_array

def ma_n(input_array, n_list=[10, 20, 50, 200]):
    ma_list = []
    for n in n_list:
        ma_list.append(ta.EMA(input_array, timeperiod=n))
    return pd.concat(ma_list, columns=list(map(lambda x:'ma{0}'.format(x), n_list)))

# endregion indicators
