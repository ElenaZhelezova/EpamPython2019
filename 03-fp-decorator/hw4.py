import datetime


def make_cache(time_arg):
    def decorator(func):
        def inner(*args):
            time_now = datetime.datetime.now()
            if args not in cached:
                cache_time = time_now + datetime.timedelta(seconds=time_arg)
                result = func(*args)
                cached[args] = [cache_time, result]
            for i in cached:
                if cached[i][0] < time_now:
                    del cached[i]
            return cached[args][1]
        cached = {}
        return inner
    return decorator


@make_cache(30)
def slow_function(n):
    return slow_function(n-1)*n if n > 1 else 1
