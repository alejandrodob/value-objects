from .exceptions import FieldMutationAttempt

def _eq(me, other):
    if isinstance(other, me.__class__):
        for field in me.__fields__:
            if not (hasattr(other, field)
                    and getattr(me, field) == getattr(other, field)):
                return False
        return True
    else:
        return NotImplemented

def _ne(me, other):
    result = _eq(me, other)
    return result if result is NotImplemented else not result

def _setattr(me, attr, value):
    raise FieldMutationAttempt("Cannot modify field '%s'. ValueObject is immutable" % attr)

def _delattr(me, attr):
    raise FieldMutationAttempt("Cannot delete field '%s'. ValueObject is immutable" % attr)
