
from ff_utils.tools import util_tools as ut
from ff_utils.data_accessing.db import PGEngine, table_name_dict

# region datetime
def get_ak_td_array(end_date=ut.get_today_str()):
    td_df=PGEngine.table2df(table_name_dict['dc_ak_trade_date'])
    td_array = td_df['trade_date']
    return td_array[td_array<=end_date]

# endregion datetime


# region dpp_s
def is_ak_daily_updated():
    
    pass


# endregion dpp_s


