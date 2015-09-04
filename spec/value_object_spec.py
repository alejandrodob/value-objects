import value_object
from expects import *


class Point(object):
    __metaclass__ = value_object.ValueObject
    __fields__ = ('x', 'y')


with description(value_object.ValueObject):

    with description("standard behaviour"):
        with context('with keyword arguments in constructor'):
            with it('generates instance attributes for declared fields'):
                a_value_object = Point(x=5, y=3)

                expect(a_value_object.x).to(equal(5))
                expect(a_value_object.y).to(equal(3))

            with it('raises an exception for non declared fields'):
                def create_point_with_invalid_field():
                    Point(not_a_field="whatever")

                expect(create_point_with_invalid_field).to(raise_error(ValueError))

        with context('with non-keyword arguments in constructor'):
            with it('generates instance attributes for declared fields'):
                a_value_object = Point(5, 3)

                expect(a_value_object.x).to(equal(5))
                expect(a_value_object.y).to(equal(3))

        with context("with mixed arguments and keyword arguments"):
            with it('generates instance attributes for declared fields'):
                a_value_object = Point(5, y=3)

                expect(a_value_object.x).to(equal(5))
                expect(a_value_object.y).to(equal(3))

    with description("restrictions"):
        with context('on initialization'):
            with it("must at least have one field"):
                class NoFields(object):
                    __metaclass__ = value_object.ValueObject
                    __fields__ = ()

                expect(NoFields).to(raise_error(ValueError))

            with it("must not have any field initialized to None"):
                def create_point_with_None_argument():
                    Point(None, 3)

                expect(create_point_with_None_argument).to(raise_error(ValueError))

            with it('must have number of values equal to number of fields'):
                def create_point_with_too_many_values():
                    Point(5, 3, 4)
                def create_point_with_not_enough_values():
                    Point(5)

                expect(create_point_with_too_many_values).to(raise_error(ValueError))
                expect(create_point_with_not_enough_values).to(raise_error(ValueError))

            with _it("must respect order of declared fields"):
                def create_point_with_invalid_fields_order():
                    Point(3, x=5)

                expect(create_point_with_invalid_fields_order).to(raise_error(ValueError))
