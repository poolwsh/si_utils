

from enum import Enum, unique
from ff_utils.data_accessing.db import table_name_dict

s_pre = 100000000 # 8*0
i_pre = 200000000 # 8*0

@unique
class s_indicator(Enum):
    sctr = 1001 + s_pre
    scsc = 1002 + s_pre
    p1y_d = 2011 + s_pre
    p1y_c = 2012 + s_pre
    p2y_d = 2021 + s_pre
    p2y_c = 2022 + s_pre
    v1y_d = 2111 + s_pre
    v1y_c = 2112 + s_pre
    v2y_d = 2121 + s_pre
    v2y_c = 2122 + s_pre
    ma5 = 3005 + s_pre
    ma10 = 3010 + s_pre
    ma20 = 3020 + s_pre
    ma30 = 3030 + s_pre
    ma40 = 3040 + s_pre
    ma50 = 3050 + s_pre
    ma100 = 3100 + s_pre
    ma110 = 3110 + s_pre
    ma120 = 3120 + s_pre
    ma130 = 3130 + s_pre
    ma140 = 3140 + s_pre
    ma150 = 3150 + s_pre
    ma200 = 3200 + s_pre
    ma210 = 3210 + s_pre
    ma220 = 3220 + s_pre
    ma230 = 3230 + s_pre
    ma240 = 3240 + s_pre
    ma250 = 3250 + s_pre

@unique
class i_indicator(Enum):
    sctr = 1001 + i_pre
    scsc = 1002 + i_pre
    ma5 = 3005 + i_pre
    ma10 = 3010 + i_pre
    ma20 = 3020 + i_pre
    ma30 = 3030 + i_pre
    ma40 = 3040 + i_pre
    ma50 = 3050 + i_pre
    ma100 = 3100 + i_pre
    ma110 = 3110 + i_pre
    ma120 = 3120 + i_pre
    ma130 = 3130 + i_pre
    ma140 = 3140 + i_pre
    ma150 = 3150 + i_pre
    ma200 = 3200 + i_pre
    ma210 = 3210 + i_pre
    ma220 = 3220 + i_pre
    ma230 = 3230 + i_pre
    ma240 = 3240 + i_pre
    ma250 = 3250 + i_pre
    trend = 4001 + i_pre

s_indicator_dict_f = {
    'sctr':'sctr',
    'scsc':'sctr_score',
    'p1y_d': 'peak_1year_days',
    'p1y_c':'peak_1year_change',
    'p2y_d': 'peak_2year_days',
    'p2y_c':'peak_2year_change',
    'v1y_d': 'valley_1year_days',
    'v1y_c':'valley_1year_change',
    'v2y_d': 'valley_2year_days',
    'v2y_c':'valley_2year_change',
    'sma10':'s_ma10',
    'sma20':'s_ma20',
    'sma50':'s_ma50',
    'sma150':'s_ma150',
    'sma200':'s_ma200',
}

s_indicator_dict_i = {
    'stick2': 'is_stick2',
    'mm_tt1': 'is_mm_tt1',
    
}

# s_row_indicator_dict = {
#     'is_stick2': 'smallint',
#     'is_mm_tt1': 'smallint',
#     'sctr':'real',
#     'peak_1year_days': 'smallint',
#     'peak_1year_change':'real',
#     'peak_2year_days': 'smallint',
#     'peak_2year_change':'real',
#     'ma10':'real',
#     'ma20':'real',
#     'ma50':'real',
#     'ma150':'real',
#     'ma200':'real',
# }

# s_col_indicator_dict = {
#     'sctr_score':'real',
# }
i_indicator_dict_f = {
    'sctr':'sctr',
    'scsc':'sctr_score',
    'sma10':'s_ma10',
    'sma20':'s_ma20',
    'sma50':'s_ma50',
    'sma150':'s_ma150',
    'sma200':'s_ma200',
}
i_indicator_dict_i = {
    'trend': 'trend'
}
# i_indicator_dict = {
#     'trend': 'smallint',
#     'sctr':'real',
#     'ma10':'real',
#     'ma20':'real',
#     'ma50':'real',
#     'ma150':'real',
#     'ma200':'real',
# }

# i_indicator_dict = {
#     'sctr_score':'real',
# }












