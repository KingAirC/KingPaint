import functools
from .king_decorater import geometry_generate
from ..geometry.king_empty_geometry import EmptyGeometry


def geometries_generate(classes=(), numbers=()):
    def actual_decorator(func):
        @functools.wraps(func)
        def process(depends=(), essential_data=None):
            @geometry_generate(cls=EmptyGeometry)
            def empty_geo_gen(depends=(), essential_data=None):
                return func(depends=depends, essential_data=essential_data)

            empty_geo = empty_geo_gen(depends=depends, essential_data=essential_data)
            geo_list = []
            s = 0
            for i in range(len(classes)):
                for j in range(numbers[i]):
                    @geometry_generate(cls=classes[i])
                    def every_geo_gen(depends=(), essential_data=None):
                        return depends[0].basic_data[essential_data[0]]

                    every_obj = every_geo_gen(depends=[empty_geo], essential_data=[s])
                    geo_list.append(every_obj)
                    s += 1
            return geo_list

        return process

    return actual_decorator
