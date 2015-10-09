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

class FieldMutationAttempt(Exception):
    pass
