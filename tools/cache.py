import redis
from ff_utils.config.base_config import RedisDB
from ff_utils.config import local_config as l_con
from functools import partial

default_cache_expire = 60 * 60 * 6 # 6 hours

class Cache(object):
    redis_default_ttl = 60 * 60 * 24
    def __init__(self, db, password, host='localhost', port=6379):
        self.host = host
        self.port = port
        self.db = db
        self.password = password

    def get_connect(self):
        if self.password is None:
            pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, decode_responses=True)
        else:
            pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db, password=self.password, decode_responses=True)
        return redis.Redis(connection_pool=pool)

def cache_get_value(cache, key):
    return cache.get(key)

def cache_set_value(cache, key, value, expire=default_cache_expire):
    cache.set(key, value)
    cache.expire(key, expire)

dc_cache = Cache(db=RedisDB.DC.value, password=l_con.redis_password, host=l_con.redis_hostname, port=l_con.redis_port).get_connect()
dpp_cache = Cache(db=RedisDB.DPP.value, password=l_con.redis_password, host=l_con.redis_hostname, port=l_con.redis_port).get_connect()

dc_cache_get_value = partial(cache_get_value, dc_cache)
dc_cache_set_value = partial(cache_set_value, dc_cache)
dpp_cache_get_value = partial(cache_get_value, dpp_cache)
dpp_cache_set_value = partial(cache_set_value, dpp_cache)










