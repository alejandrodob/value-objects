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
                raise UndeclaredField("Field '%s' not declared" % field)
            setattr(obj, field, kwargs[field])
        try:
            for invariant in self.__invariants__:
                try:
                    if not getattr(obj, invariant)():
                        raise ValueError
                except AttributeError as e:
                    raise ValueError
        except AttributeError as e:
            pass
        return obj


class UndeclaredField(Exception):
    pass
