
from ff_utils.data_accessing.db import table_name_dict

s_row_indicator_dict = {
    'is_2stick': 'smallint',
    'is_mm_tt_1': 'smallint',
    'high_1year_days': 'smallint',
    'high_1year_change':'real',
    'high_2year_days': 'smallint',
    'high_2year_change':'real',
    'sctr':'real',
    'ma10':'real',
    'ma20':'real',
    'ma50':'real',
    'ma200':'real',
}

s_col_indicator_dict = {
    'sctr_score':'real',
}

i_indicator_dict = {
    'trend': 'smallint',
    'sctr':'real',
    'ma10':'real',
    'ma20':'real',
    'ma50':'real',
    'ma200':'real',
}

i_indicator_dict = {
    'sctr_score':'real',
}

cache_name_dict = {
    'dc_ak_s_daily_realtime':'dc_ak@s_daily@realtime',
}










