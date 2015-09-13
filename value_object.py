class ValueObject(type):

    def __call__(self, *args, **kwargs):

        self._check_fields_declared()
        self._check_fields_have_value(*args, **kwargs)
        self._check_one_value_per_field_provided(*args, **kwargs)

        value_object = self._create_object_with_values(*args, **kwargs)

        self._add_equality_comparators_to(value_object)

        self._check_invariants(value_object)

        return value_object

    def _check_fields_declared(self):
        if not self.__fields__:
            raise NoFieldsDeclared()

    def _check_fields_have_value(self, *args, **kwargs):
        if None in args:
            field = self.__fields__[args.index(None)]
            raise FieldWithoutValue("Declared field '%s' must have a value" % field)
        none_keyword_args = [k for k, v in kwargs.iteritems() if v == None]
        if none_keyword_args:
            raise FieldWithoutValue("Declared field '%s' must have a value" % none_keyword_args[0])

    def _check_one_value_per_field_provided(self, *args, **kwargs):
        total_values_provided = len(args) + len(kwargs)
        if total_values_provided != len(self.__fields__):
            raise WrongNumberOfArguments("2 fields were declared, but constructor received %s" % total_values_provided)

    def _create_object_with_values(self, *args, **kwargs):
        value_object = type.__call__(self)
        self._add_values_to_value_object(value_object, *args, **kwargs)
        return value_object

    def _add_values_to_value_object(self, value_object, *args, **kwargs):
        if args:
            for value, field in zip(args, self.__fields__):
                setattr(value_object, field, value)
        for field in kwargs:
            if field not in self.__fields__:
                raise WrongField("Field '%s' not declared" % field)
            setattr(value_object, field, kwargs[field])

    def _add_equality_comparators_to(self, value_object):
        object_class = value_object.__class__
        def eq(self, other):
            if isinstance(other, object_class):
                for field in self.__fields__:
                    if not (hasattr(other, field)
                            and getattr(self, field) == getattr(other, field)):
                        return False
                return True
            else:
                return NotImplemented
        def ne(self, other):
            result = eq(self, other)
            return result if result is NotImplemented else not result

        setattr(object_class, '__eq__', eq)
        setattr(object_class, '__ne__', ne)

    def _check_invariants(self, value_object):
        if '__invariants__' not in dir(self):
            return
        self._check_declared_invariants_are_implemented(value_object)
        self._check_invariants_hold(value_object)

    def _check_declared_invariants_are_implemented(self, value_object):
        for invariant in self.__invariants__:
            try:
                getattr(value_object, invariant)
            except AttributeError as e:
                raise InvariantNotImplemented( "Invariant '%s' declared but not implemented" % invariant)

    def _check_invariants_hold(self, value_object):
        for invariant in self.__invariants__:
            if not getattr(value_object, invariant)():
                raise InvariantViolation("Fields %s violate invariant '%s'" % (self.__fields__, invariant))


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

class InvariantNotImplemented(Exception):
    pass
