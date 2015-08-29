class ValueObject(type):

    def __call__(self, *args, **kwargs):
        obj = type.__call__(self, *args)
        for field in kwargs:
            if field not in self.__fields__:
                raise ValueError
            setattr(obj, field, kwargs[field])
        return obj

