from logging import info, getLogger, Formatter, StreamHandler, INFO




def logging_info(f):
    def wrap(*args, **kwargs):
        info(f"callable {f.__name__} with args({', '.join(args)}) and kwargs {kwargs}")
        return f(*args, **kwargs)
    return wrap

def logging_info_async(f):
    async def wrap(*args, **kwargs):
        info(f"callable {f.__name__} with args({', '.join(args)}) and kwargs {kwargs}")
        return await f(*args, **kwargs)
    return wrap
