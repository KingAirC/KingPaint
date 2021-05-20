import functools


def singleton(cls):
    _instance = {}

    def _singleton(*args, **kwargs):
        if cls not in _instance:
            _instance[cls] = cls(*args, **kwargs)
        return _instance[cls]

    return _singleton


def geometry_generate(cls=None, calc_essential_data_by_delta=None):
    def actual_decorator(func):
        @functools.wraps(func)
        def process(depends=(), essential_data=None):
            obj = cls(depends=depends, essential_data=essential_data, create_type=2)
            obj.calc_essential_data_by_delta = calc_essential_data_by_delta
            obj.generate_basic_data = func
            obj.init()
            return obj

        return process

    return actual_decorator
