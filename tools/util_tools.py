

import talib as ta
import pandas as pd
import orjson


from ff_utils.tools import util_tools as ut
from ff_utils.data_accessing.db import PGEngine, table_name_dict
from si_utils.config import base_config as con
from si_utils.tools import cache

# region datetime
def get_ak_td_array(end_date=ut.get_today_str()):
    td_df=PGEngine.table2df(table_name_dict['dc_ak_trade_date'])
    td_array = td_df['trade_date']
    return td_array[td_array<=end_date]

# endregion datetime


# region dpp_s
def get_cached_ak_s_daily():
    ak_daily_keys = [x for x in cache.dc_cache.keys() if x.startswith('dc_ak@') and x.endswith('@daily')]
    ak_daily_values = list(map(lambda x:orjson.loads(orjson.loads(cache.dc_cache_get_value(x))['data_value']), ak_daily_keys))
    ak_daily_df = pd.DataFrame(ak_daily_values)
    return ak_daily_df


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
