class ValueObject(type):

    def __call__(self, *args, **kwargs):
        if not self.__fields__:
            raise FieldsNotDeclared()
        if None in args:
            field = self.__fields__[args.index(None)]
            raise FieldWithoutValue("Declared field '%s' must have a value" % field)
        none_keyword_args = [k for k, v in kwargs.iteritems() if v == None]
        if none_keyword_args:
            raise FieldWithoutValue("Declared field '%s' must have a value" % none_keyword_args[0])
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

class FieldsNotDeclared(Exception):
    pass

class FieldWithoutValue(Exception):
    pass
