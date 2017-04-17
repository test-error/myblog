import memcache


cache = memcache.Client(['127.0.0.1:11211'],debug=True)



def set(key=None,value=None,timeout=60):
    if key and value:
        result = cache.set(key,value,timeout)
        return result
    return False

def get(key=None):
    if key:
        return cache.get(key)
    return None

def delete(key=None):
    if key:
        cache.delete(key)
        return True
    return False