from .exceptions import *
from .magic_methods import _eq, _ne, _setattr, _delattr

class ValueObject(type):

    def __call__(self, *args, **kwargs):
        self._open_class_for_modification()
        self._check_fields_have_value(*args, **kwargs)
        self._check_one_value_per_field_provided(*args, **kwargs)

        value_object = self._create_object_with_values(*args, **kwargs)
        self._add_equality_comparators_to(value_object)
        self._check_invariants(value_object)
        self._close_class_for_modification()

        return value_object

    def _check_fields_have_value(self, *args, **kwargs):
        if None in args:
            field = self.__fields__[args.index(None)]
            raise FieldWithoutValue("Declared field '%s' must have a value" % field)
        none_keyword_args = [k for k, v in kwargs.iteritems() if v == None]
        if none_keyword_args:
            raise FieldWithoutValue("Declared field '%s' must have a value" % none_keyword_args[0])

    def _check_one_value_per_field_provided(self, *args, **kwargs):
        total_values_provided = len(args) + len(kwargs)
        values_declared = len(self.__fields__)
        if total_values_provided != values_declared:
            raise WrongNumberOfArguments("%s fields were declared, but constructor received %s" % (values_declared, total_values_provided))

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
            if hasattr(value_object, field):
                raise TypeError("%s constructor got multiple values for keyword argument '%s'"
                                % (value_object.__class__.__name__, field))
            setattr(value_object, field, kwargs[field])

    def _add_equality_comparators_to(self, value_object):
        setattr(self, '__eq__', _eq)
        setattr(self, '__ne__', _ne)

    def _open_class_for_modification(self):
        setattr(self, '__setattr__', object.__setattr__)

    def _close_class_for_modification(self):
        setattr(self, '__delattr__', _delattr)
        setattr(self, '__setattr__', _setattr)

    def _check_invariants(self, value_object):
        if hasattr(self, '__invariants__'):
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


def value_object(*fields):
    if len(fields) < 1:
        raise NoFieldsDeclared()

    def the_class(a_class):
        class DecoratedClass(object):
            __metaclass__ = ValueObject
            __fields__ = fields

        DecoratedClass.__name__ = a_class.__name__
        DecoratedClass.__module__ = a_class.__module__
        if hasattr(a_class, '__invariants__'):
            DecoratedClass.__invariants__ = a_class.__invariants__
            for invariant in a_class.__invariants__:
                if hasattr(a_class, invariant):
                    setattr(DecoratedClass, invariant, getattr(a_class, invariant).im_func)
        del a_class
        return DecoratedClass
    return the_class
