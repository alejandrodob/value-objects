import value_object

class Point(object):
    __metaclass__ = value_object.ValueObject


with description(value_object.ValueObject):

    with description("standard behaviour"):

        with context('with keyword arguments in constructor'):

            with it('generates constructor, fields and accessors for declared fields'):
                a_value_object = Point(x=5, y=3)

                assert a_value_object.x == 5
                assert a_value_object.y == 3
