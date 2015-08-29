class ValueObject(type):

    def __call__(self, *args, **kwargs):
        obj = type.__call__(self, *args)
        for field in kwargs:
            setattr(obj, field, kwargs[field])
        return obj

