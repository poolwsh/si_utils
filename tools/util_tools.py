

import talib as ta
import pandas as pd
import orjson
from datetime import datetime, timedelta

from ff_utils.tools import util_tools as ut
from ff_utils.data_accessing.db import PGEngine, table_name_dict
from si_utils.config import base_config as con
from si_utils.config.data_structure import cache_name_dict
from si_utils.tools import cache



# region datetime
date_format = '%Y-%m-%d'

def get_ak_td_array(end_date=ut.get_today_str()):
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

def get_ak_no_trade_days(start_date=None, end_date=ut.get_today_str()):
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
