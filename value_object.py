class ValueObject(type):

    def __call__(self, *args, **kwargs):
        obj = type.__call__(self)
        if len(args) > len(self.__fields__):
            raise ValueError
        if args:
            for field_value in zip(args, self.__fields__):
                setattr(obj, field_value[1], field_value[0])
        for field in kwargs:
            if field not in self.__fields__:
                raise ValueError
            setattr(obj, field, kwargs[field])
        return obj
