class ValueObject(type):

    def __call__(self, *args, **kwargs):
        if not self.__fields__:
            raise ValueError
        if None in args or None in kwargs.values():
            raise ValueError
        obj = type.__call__(self)
        total_values_provided = len(args) + len(kwargs)
        if total_values_provided != len(self.__fields__):
            raise ValueError
        if args:
            for field_value in zip(args, self.__fields__):
                setattr(obj, field_value[1], field_value[0])
        for field in kwargs:
            if field not in self.__fields__:
                raise ValueError
            setattr(obj, field, kwargs[field])
        return obj
