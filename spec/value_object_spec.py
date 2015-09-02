import value_object

class Point(object):
    __metaclass__ = value_object.ValueObject
    __fields__ = ('x', 'y')

with description(value_object.ValueObject):

    with description("standard behaviour"):

        with context('with keyword arguments in constructor'):

            with it('generates instance attributes for declared fields'):
                a_value_object = Point(x=5, y=3)

                assert a_value_object.x == 5
                assert a_value_object.y == 3

            with it('raises an exception for non declared fields'):
                try:
                    a_value_object = Point(not_a_field="whatever")
                except ValueError, e:
                    assert True
                else:
                    assert False, "Exception not raised"

        with context('with non-keyword arguments in constructor'):

            with it('generates instance attributes for declared fields'):
                a_value_object = Point(5, 3)

                assert a_value_object.x == 5
                assert a_value_object.y == 3


    with description("restrictions"):

        with context('on initialization'):

            with it('must have number of values equal to number of fields'):
                try:
                    a_value_object = Point(5, 3, 4)
                except ValueError, e:
                    assert True
                else:
                    assert False, "Exception not raised"

                try:
                    a_value_object = Point(5)
                except ValueError, e:
                    assert True
                else:
                    assert False, "Exception not raised"
