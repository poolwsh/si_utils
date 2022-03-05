
from ff_utils.data_accessing.db import table_name_dict

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












