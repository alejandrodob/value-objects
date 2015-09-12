class ValueObject(type):

    def __call__(self, *args, **kwargs):
        if not self.__fields__:
            raise NoFieldsDeclared()
        if None in args:
            field = self.__fields__[args.index(None)]
            raise FieldWithoutValue("Declared field '%s' must have a value" % field)
        none_keyword_args = [k for k, v in kwargs.iteritems() if v == None]
        if none_keyword_args:
            raise FieldWithoutValue("Declared field '%s' must have a value" % none_keyword_args[0])
        obj = type.__call__(self)
        total_values_provided = len(args) + len(kwargs)
        if total_values_provided != len(self.__fields__):
            raise WrongNumberOfArguments("2 fields were declared, but constructor received %s" % total_values_provided)
        if args:
            for field_value in zip(args, self.__fields__):
                setattr(obj, field_value[1], field_value[0])
        for field in kwargs:
            if field not in self.__fields__:
                raise WrongField("Field '%s' not declared" % field)
            setattr(obj, field, kwargs[field])
        try:
            for invariant in self.__invariants__:
                try:
                    if not getattr(obj, invariant)():
                        raise InvariantViolation("Fields %s violate invariant '%s'" % (self.__fields__, invariant))
                except AttributeError as e:
                    raise ValueError
        except AttributeError as e:
            pass
        return obj


class WrongField(Exception):
    pass

class NoFieldsDeclared(Exception):
    pass

class FieldWithoutValue(Exception):
    pass

class WrongNumberOfArguments(Exception):
    pass

class InvariantViolation(Exception):
    pass
