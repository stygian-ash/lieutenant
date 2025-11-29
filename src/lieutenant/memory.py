'''Tools for caching/memoizing functions and datastructures.'''
from functools import lru_cache

from diskcache import Cache
from platformdirs import user_cache_path

CACHE_DIR = user_cache_path() / 'python-lieutenant'

cache = Cache(CACHE_DIR)

def memoize(func):
    '''Memoize to disk decorator.'''
    return lru_cache(maxsize=None)(cache.memoize()(func))
