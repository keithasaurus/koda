import re
from dataclasses import dataclass
from datetime import date
from typing import Any, Dict, List, Protocol, Tuple

from koda.either import First, Second, Third
from koda.json.validation import (BLANK_STRING_MSG, OBJECT_ERRORS_FIELD, ArrayOf, Boolean,
                                  Date, Email, Enum, Float, Integer, Jsonable, Lazy,
                                  MapOf, Maximum, MaxItems, MaxLength, MaxProperties,
                                  Minimum, MinItems, MinLength, MinProperties, MultipleOf,
                                  NotBlank, Null, Nullable, Obj1, Obj2, Obj3, Obj4, Obj5,
                                  Obj6, Obj7, Obj8, Obj9, Obj10, OneOf2, OneOf3,
                                  RegexValidator, String, Tuple2, Tuple3,
                                  deserialize_and_validate, fail, fail_list, key,
                                  maybe_key, unique_items, unwrap_jsonable)
from koda.maybe import Just, Maybe, Nothing
from koda.result import Failure, Result, Success
from koda.validation import PredicateValidator


def test_float_() -> None:
    assert Float()("a string") == fail_list("expected a float")

    assert Float()(5.5) == Success(5.5)

    assert Float()(4) == fail_list("expected a float")

    assert Float(Maximum(500.0))(503.0) == fail_list(
        "Maximum allowed value is 500.0")

    assert Float(Maximum(500.0))(3.5) == Success(3.5)

    assert Float(Minimum(5.0))(4.999) == fail_list("Minimum allowed value is 5.0")

    assert Float(Minimum(5.0))(5.0) == Success(5.0)

    class MustHaveAZeroSomewhere(PredicateValidator[float, Jsonable]):
        def is_valid(self, val: float) -> bool:
            for char in str(val):
                if char == '0':
                    return True
            else:
                return False

        def fail_message(self, val: float) -> Jsonable:
            return Jsonable("There should be a zero in the number")

    assert Float(Minimum(2.5),
                 Maximum(4.0),
                 MustHaveAZeroSomewhere())(5.5) == fail_list(
        'Maximum allowed value is 4.0',
        'There should be a zero in the number'
    )


def test_boolean() -> None:
    assert Boolean()("a string") == fail_list("expected a boolean")

    assert Boolean()(True) == Success(True)

    assert Boolean()(False) == Success(False)

    class RequireTrue(PredicateValidator[bool, Jsonable]):
        def is_valid(self, val: bool) -> bool:
            return val is True

        def fail_message(self, val: bool) -> Jsonable:
            return Jsonable("must be true")

    assert Boolean(RequireTrue())(False) == fail_list("must be true")

    assert Boolean()(1) == fail_list("expected a boolean")


def test_date() -> None:
    default_date_failure = fail(["expected date formatted as yyyy-mm-dd"])
    assert Date()("2021-03-21") == Success(date(2021, 3, 21))
    assert Date()("2021-3-21") == default_date_failure


def test_null() -> None:
    assert Null("a string") == fail_list("expected null")

    assert Null(None) == Success(None)

    assert Null(False) == fail_list("expected null")


def test_integer() -> None:
    assert Integer()("a string") == fail_list("expected an integer")

    assert Integer()(5) == Success(5)

    assert Integer()(True) == fail_list("expected an integer"), \
        "even though `bool`s are subclasses of ints in python, we wouldn't " \
        "want to validate incoming data as ints if they are bools"

    assert Integer()("5") == fail_list("expected an integer")

    assert Integer()(5.0) == fail_list("expected an integer")

    class DivisibleBy2(PredicateValidator[int, Jsonable]):
        def is_valid(self, val: int) -> bool:
            return val % 2 == 0

        def fail_message(self, val: int) -> Jsonable:
            return Jsonable("must be divisible by 2")

    assert Integer(
        Minimum(2),
        Maximum(10),
        DivisibleBy2(),
    )(11) == fail_list("Maximum allowed value is 10",
                       "must be divisible by 2")


def test_array_of() -> None:
    assert ArrayOf(Float())("a string") == \
           fail({"invalid type": ["expected an array"]})

    assert ArrayOf(Float())([5.5, "something else"]) == \
           fail({"index 1": ["expected a float"]})

    assert ArrayOf(Float())([5.5, 10.1]) == Success([5.5, 10.1])

    assert ArrayOf(Float())([]) == Success([])

    assert ArrayOf(
        Float(Minimum(5.5)),
        MinItems(1),
        MaxItems(3)
    )([10.1, 7.7, 2.2, 5]) == fail(
        {"index 2": ["Minimum allowed value is 5.5"],
         "index 3": ["expected a float"],
         "__array__": ["maximum allowed length is 3"]}
    )


def test_maybe_val() -> None:
    assert Nullable(String())(None) == Success(Nothing)
    assert Nullable(String())(5) == fail(["expected a string"])
    assert Nullable(String())("okok") == Success(Just("okok"))


def test_map_of() -> None:
    assert MapOf(String(), String())(5) == fail(
        {"invalid type": ["expected a map"]}
    )

    assert MapOf(String(), String())({}) == Success({})

    assert MapOf(String(), Integer())({"a": 5, "b": 22}) == Success({"a": 5, "b": 22})

    @dataclass(frozen=True)
    class MaxKeys(PredicateValidator[Dict[Any, Any], Jsonable]):
        max: int

        def is_valid(self, val: Dict[Any, Any]) -> bool:
            return len(val) <= self.max

        def fail_message(self, val: Dict[Any, Any]) -> Jsonable:
            return Jsonable(f"max {self.max} key(s) allowed")

    complex_validator = MapOf(String(MaxLength(4)),
                              Integer(Minimum(5)),
                              MaxKeys(1))
    assert complex_validator(
        {"key1": 10,
         "key1a": 2},
    ) == fail({
        "key1a": ["Minimum allowed value is 5"],
        "key1a (key)": ["maximum allowed length is 4"],
        "__object__": ["max 1 key(s) allowed"]
    })

    assert complex_validator({"a": 100}) == Success({"a": 100})

    assert MapOf(String(),
                 Integer(),
                 MaxKeys(1))(
        {OBJECT_ERRORS_FIELD: "not an int",
         "b": 1}
    ) == Failure(
        Jsonable(
            {OBJECT_ERRORS_FIELD: Jsonable(
                [Jsonable("max 1 key(s) allowed"),
                 Jsonable([Jsonable("expected an integer")])])})
    ), ("we need to make sure that errors are not lost even if there are key naming "
        "collisions with the object field")


def test_string() -> None:
    assert String()(False) == fail_list("expected a string")

    assert String()("abc") == Success("abc")

    assert String(MaxLength(3))("something") == \
           fail_list("maximum allowed length is 3")

    min_len_3_not_blank_validator = String(MinLength(3),
                                           NotBlank())

    assert min_len_3_not_blank_validator("") == \
           fail_list("minimum allowed length is 3",
                     "cannot be blank")

    assert min_len_3_not_blank_validator("   ") == \
           fail_list("cannot be blank")

    assert min_len_3_not_blank_validator("something") == Success("something")


def test_max_string_length() -> None:
    assert MaxLength(0)("") == Success("")

    try:
        MaxLength(-1)
    except AssertionError:
        pass
    else:
        raise AssertionError("should have raised error in try call")

    assert MaxLength(5)("abc") == Success("abc")

    assert MaxLength(5)("something") == fail("maximum allowed length is 5")


def test_min_string_length() -> None:
    assert MinLength(0)("") == Success("")

    try:
        MinLength(-1)
    except AssertionError:
        pass
    else:
        raise AssertionError("should have raised error in try call")

    assert MinLength(3)("abc") == Success("abc")

    assert MinLength(3)("zz") == fail("minimum allowed length is 3")


def test_max_items() -> None:
    assert MaxItems(0)([]) == Success([])

    try:
        MaxItems(-1)
    except AssertionError:
        pass
    else:
        raise AssertionError("should have raised error in try call")

    assert MaxItems(5)([1, 2, 3]) == Success([1, 2, 3])

    assert MaxItems(5)(["a", "b", "c", "d", "e", "fghij"]) == \
           fail("maximum allowed length is 5")


def test_min_items() -> None:
    assert MinItems(0)([]) == Success([])

    try:
        MinItems(-1)
    except AssertionError:
        pass
    else:
        raise AssertionError("should have raised error in try call")

    assert MinItems(3)([1, 2, 3]) == Success([1, 2, 3])

    assert MinItems(3)([1, 2]) == fail("minimum allowed length is 3")


def test_max_properties() -> None:
    assert MaxProperties(0)({}) == Success({})

    try:
        MaxProperties(-1)
    except AssertionError:
        pass
    else:
        raise AssertionError("should have raised error in try call")

    assert MaxProperties(5)({"a": 1, "b": 2, "c": 3}) == Success({"a": 1, "b": 2, "c": 3})

    assert MaxProperties(1)({"a": 1, "b": 2}) == fail("maximum allowed properties is 1")


def test_min_properties() -> None:
    assert MinProperties(0)({}) == Success({})

    try:
        MinProperties(-1)
    except AssertionError:
        pass
    else:
        raise AssertionError("should have raised error in try call")

    assert MinProperties(3)({"a": 1, "b": 2, "c": 3}) == Success({"a": 1, "b": 2, "c": 3})

    assert MinProperties(3)({"a": 1, "b": 2}) == fail("minimum allowed properties is 3")


def test_tuple2() -> None:
    assert Tuple2(String(), Integer())({}) == \
           fail({"invalid type": ["expected array of length 2"]})

    assert Tuple2(String(), Integer())([]) == \
           fail({"invalid type": ["expected array of length 2"]})

    assert Tuple2(String(), Integer())(["a", 1]) == Success(("a", 1))

    assert Tuple2(String(), Integer())([1, "a"]) == fail({
        "index 0": ["expected a string"],
        "index 1": ["expected an integer"]
    })

    def must_be_a_if_integer_is_1(ab: Tuple[str, int]) -> Result[
        Tuple[str, int],
        Jsonable
    ]:
        if ab[1] == 1:
            if ab[0] == "a":
                return Success(ab)
            else:
                return fail({"__array__": ["must be a if int is 1"]})
        else:
            return Success(ab)

    a1_validator = Tuple2(String(), Integer(), must_be_a_if_integer_is_1)

    assert a1_validator(["a", 1]) == Success(("a", 1))
    assert a1_validator(["b", 1]) == fail(
        {"__array__": ["must be a if int is 1"]}
    )
    assert a1_validator(["b", 2]) == Success(("b", 2))


def test_tuple3() -> None:
    assert Tuple3(String(), Integer(), Boolean())({}) == \
           fail({"invalid type": ["expected array of length 3"]})

    assert Tuple3(String(), Integer(), Boolean())([]) == \
           fail({"invalid type": ["expected array of length 3"]})

    assert Tuple3(String(), Integer(), Boolean())(["a", 1, False]) == \
           Success(("a", 1, False))

    assert Tuple3(String(), Integer(), Boolean())([1, "a", 7.42]) == fail({
        "index 0": ["expected a string"],
        "index 1": ["expected an integer"],
        "index 2": ["expected a boolean"]
    })

    def must_be_a_if_1_and_true(abc: Tuple[str, int, bool]) -> Result[
        Tuple[str, int, bool],
        Jsonable
    ]:
        if abc[1] == 1 and abc[2] is True:
            if abc[0] == "a":
                return Success(abc)
            else:
                return fail(
                    {"__array__": ["must be a if int is 1 and bool is True"]}
                )
        else:
            return Success(abc)

    a1_validator = Tuple3(String(), Integer(), Boolean(), must_be_a_if_1_and_true)

    assert a1_validator(["a", 1, True]) == Success(("a", 1, True))
    assert a1_validator(["b", 1, True]) == fail(
        {"__array__": ["must be a if int is 1 and bool is True"]}
    )
    assert a1_validator(["b", 2, False]) == Success(("b", 2, False))


def test_obj_1() -> None:
    @dataclass
    class Person:
        name: str

    validator = Obj1(
        key("name", String()),
        into=Person
    )

    assert validator("not a dict") == fail(
        {"__object__": ["expected an object"]}
    )

    assert validator({}) == fail({"name": ["key missing"]})

    assert validator({"name": 5}) == fail({"name": ["expected a string"]})

    assert validator({"name": "bob", "age": 50}) == \
           fail({"__object__":
                 ["Received unknown keys. Only expected ['name']"]})

    assert validator({"name": "bob"}) == Success(Person("bob"))


def test_obj_2() -> None:
    @dataclass
    class Person:
        name: str
        age: Maybe[int]

    validator = Obj2(
        key("name", String()),
        maybe_key("age", Integer()),
        into=Person
    )

    assert validator("not a dict") == fail(
        {"__object__": ["expected an object"]}
    )

    assert validator({}) == fail({"name": ["key missing"]})

    assert validator({"name": 5, "age": "50"}) == fail({
        "name": ["expected a string"],
        "age": ["expected an integer"]
    })

    assert validator({"name": "bob", "age": 50, "eye_color": "brown"}) == \
           fail({"__object__":
                 ["Received unknown keys. Only expected ['age', 'name']"]})

    assert validator({"name": "bob", "age": 50}) == Success(Person("bob", Just(50)))
    assert validator({"name": "bob"}) == Success(Person("bob", Nothing))


def test_obj_3() -> None:
    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int

    validator = Obj3(
        key("first_name", String()),
        key("last_name", String()),
        key("age", Integer()),
        into=Person
    )

    assert validator({
        "first_name": "bob",
        "last_name": "smith",
        "age": 50
    }) == Success(Person("bob", "smith", 50))

    assert validator("") == fail({"__object__": ["expected an object"]})


class PersonLike(Protocol):
    last_name: str
    eye_color: str


_JONES_ERROR_MSG = {"__object__":
                    ["can't have last_name of jones and eye color of brown"]}


def _nobody_named_jones_has_brown_eyes(person: PersonLike
                                       ) -> Result[PersonLike, Jsonable]:
    if person.last_name.lower() == 'jones' and person.eye_color == 'brown':
        return fail(_JONES_ERROR_MSG)
    else:
        return Success(person)


def test_obj_4() -> None:
    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int
        eye_color: str

    validator = Obj4(
        key("first_name", String()),
        key("last_name", String()),
        key("age", Integer()),
        key("eye color", String()),
        into=Person,
        validate_object=_nobody_named_jones_has_brown_eyes
    )

    assert validator({
        "first_name": "bob",
        "last_name": "smith",
        "age": 50,
        "eye color": "brown"
    }) == Success(Person("bob", "smith", 50, "brown"))

    assert validator({
        "first_name": "bob",
        "last_name": "Jones",
        "age": 50,
        "eye color": "brown"
    }) == fail(_JONES_ERROR_MSG)

    assert validator("") == fail({"__object__": ["expected an object"]})


def test_obj_5() -> None:
    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int
        eye_color: str
        can_fly: bool

    validator = Obj5(
        key("first_name", String()),
        key("last_name", String()),
        key("age", Integer()),
        key("eye color", String()),
        key("can-fly", Boolean()),
        into=Person,
        validate_object=_nobody_named_jones_has_brown_eyes
    )

    assert validator({
        "first_name": "bob",
        "last_name": "smith",
        "age": 50,
        "eye color": "brown",
        "can-fly": True
    }) == Success(Person("bob", "smith", 50, "brown", True))

    assert validator({
        "first_name": "bob",
        "last_name": "Jones",
        "age": 50,
        "eye color": "brown",
        "can-fly": True
    }) == fail(_JONES_ERROR_MSG)

    assert validator("") == fail({"__object__": ["expected an object"]})


def test_obj_6() -> None:
    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int
        eye_color: str
        can_fly: bool
        fingers: float

    validator = Obj6(
        key("first_name", String()),
        key("last_name", String()),
        key("age", Integer()),
        key("eye color", String()),
        key("can-fly", Boolean()),
        key("number_of_fingers", Float()),
        into=Person
    )

    assert validator({
        "first_name": "bob",
        "last_name": "smith",
        "age": 50,
        "eye color": "brown",
        "can-fly": True,
        "number_of_fingers": 6.5,
    }) == Success(Person("bob",
                         "smith",
                         50,
                         "brown",
                         True,
                         6.5))

    assert validator("") == fail({"__object__": ["expected an object"]})


def test_obj_7() -> None:
    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int
        eye_color: str
        can_fly: bool
        fingers: float
        toes: float

    validator = Obj7(
        key("first_name", String()),
        key("last_name", String()),
        key("age", Integer()),
        key("eye color", String()),
        key("can-fly", Boolean()),
        key("number_of_fingers", Float()),
        key("number of toes", Float()),
        into=Person
    )

    assert validator({
        "first_name": "bob",
        "last_name": "smith",
        "age": 50,
        "eye color": "brown",
        "can-fly": True,
        "number_of_fingers": 6.5,
        "number of toes": 9.8
    }) == Success(Person("bob",
                         "smith",
                         50,
                         "brown",
                         True,
                         6.5,
                         9.8))

    assert validator("") == fail({"__object__": ["expected an object"]})


def test_obj_8() -> None:
    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int
        eye_color: str
        can_fly: bool
        fingers: float
        toes: float
        favorite_color: Maybe[str]

    validator = Obj8(
        key("first_name", String()),
        key("last_name", String()),
        key("age", Integer()),
        key("eye color", String()),
        key("can-fly", Boolean()),
        key("number_of_fingers", Float()),
        key("number of toes", Float()),
        maybe_key("favorite_color", String()),
        into=Person,
        validate_object=_nobody_named_jones_has_brown_eyes
    )

    assert validator({
        "first_name": "bob",
        "last_name": "smith",
        "age": 50,
        "eye color": "brown",
        "can-fly": True,
        "number_of_fingers": 6.5,
        "number of toes": 9.8,
        "favorite_color": "blue"
    }) == Success(Person("bob",
                         "smith",
                         50,
                         "brown",
                         True,
                         6.5,
                         9.8,
                         Just("blue")))

    assert validator({
        "first_name": "bob",
        "last_name": "smith",
        "age": 50,
        "eye color": "brown",
        "can-fly": True,
        "number_of_fingers": 6.5,
        "number of toes": 9.8,
    }) == Success(Person("bob",
                         "smith",
                         50,
                         "brown",
                         True,
                         6.5,
                         9.8,
                         Nothing))

    assert validator({
        "first_name": "bob",
        "last_name": "jones",
        "age": 50,
        "eye color": "brown",
        "can-fly": True,
        "number_of_fingers": 6.5,
        "number of toes": 9.8,
        "favorite_color": "blue"
    }) == fail(_JONES_ERROR_MSG)

    assert validator("") == fail({"__object__": ["expected an object"]})


def test_obj_9() -> None:
    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int
        eye_color: str
        can_fly: bool
        fingers: float
        toes: float
        favorite_color: Maybe[str]
        requires_none: None

    validator = Obj9(
        key("first_name", String()),
        key("last_name", String()),
        key("age", Integer()),
        key("eye color", String()),
        key("can-fly", Boolean()),
        key("number_of_fingers", Float()),
        key("number of toes", Float()),
        maybe_key("favorite_color", String()),
        key("requires_none", Null),
        into=Person,
        validate_object=_nobody_named_jones_has_brown_eyes
    )

    assert validator({
        "first_name": "bob",
        "last_name": "smith",
        "age": 50,
        "eye color": "brown",
        "can-fly": True,
        "number_of_fingers": 6.5,
        "number of toes": 9.8,
        "favorite_color": "blue",
        "requires_none": None
    }) == Success(Person("bob",
                         "smith",
                         50,
                         "brown",
                         True,
                         6.5,
                         9.8,
                         Just("blue"),
                         None))

    assert validator("") == fail({"__object__": ["expected an object"]})


def test_obj_10() -> None:
    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int
        eye_color: str
        can_fly: bool
        fingers: float
        toes: float
        favorite_color: Maybe[str]
        requires_none: None
        something_else: List[str]

    validator = Obj10(
        key("first_name", String()),
        key("last_name", String()),
        key("age", Integer()),
        key("eye color", String()),
        key("can-fly", Boolean()),
        key("number_of_fingers", Float()),
        key("number of toes", Float()),
        maybe_key("favorite_color", String()),
        key("requires_none", Null),
        key("favorite_books", ArrayOf(String())),
        into=Person,
        validate_object=_nobody_named_jones_has_brown_eyes
    )

    assert validator({
        "first_name": "bob",
        "last_name": "smith",
        "age": 50,
        "eye color": "brown",
        "can-fly": True,
        "number_of_fingers": 6.5,
        "number of toes": 9.8,
        "favorite_color": "blue",
        "requires_none": None,
        "favorite_books": ["war and peace",
                           "pale fire"]
    }) == Success(Person("bob",
                         "smith",
                         50,
                         "brown",
                         True,
                         6.5,
                         9.8,
                         Just("blue"),
                         None,
                         ["war and peace", "pale fire"]))

    assert validator("") == fail({"__object__": ["expected an object"]})


def test_unwrap_jsonable() -> None:
    assert unwrap_jsonable(Jsonable(5)) == 5
    assert unwrap_jsonable(Jsonable("ok")) == "ok"
    assert unwrap_jsonable(Jsonable(False)) is False
    assert unwrap_jsonable(Jsonable(3.3)) == 3.3
    assert unwrap_jsonable(Jsonable((Jsonable(5), Jsonable(4), Jsonable(4)))) == \
           (5, 4, 4)
    assert unwrap_jsonable(Jsonable(
        [Jsonable("a"),
         Jsonable(5),
         Jsonable({"some_key": Jsonable(1),
                   "other key": Jsonable(None)})])
    ) == ["a", 5, {"some_key": 1, "other key": None}]


def test_choices() -> None:
    validator = Enum({"a", "bc", "def"})

    assert validator("bc") == Success("bc")
    assert validator("not present") == Failure(
        Jsonable("expected one of ['a', 'bc', 'def']")
    )


def test_not_blank() -> None:
    assert NotBlank()("a") == Success("a")
    assert NotBlank()("") == Failure(BLANK_STRING_MSG)
    assert NotBlank()(" ") == Failure(BLANK_STRING_MSG)
    assert NotBlank()("\t") == Failure(BLANK_STRING_MSG)
    assert NotBlank()("\n") == Failure(BLANK_STRING_MSG)


def test_first_of2() -> None:
    str_or_int_validator = OneOf2(String(), Integer())
    assert str_or_int_validator("ok") == Success(First("ok"))
    assert str_or_int_validator(5) == Success(Second(5))
    assert str_or_int_validator(5.5) == fail(
        {"variant 1": ["expected a string"],
         "variant 2": ["expected an integer"]})

    str_or_int_validator_named = OneOf2(
        ("name", String()),
        ("age", Integer())
    )

    assert str_or_int_validator_named(5.5) == fail(
        {"name": ["expected a string"],
         "age": ["expected an integer"]}
    )


def test_first_of3() -> None:
    str_or_int_or_float_validator = OneOf3(String(), Integer(), Float())
    assert str_or_int_or_float_validator("ok") == Success(First("ok"))
    assert str_or_int_or_float_validator(5) == Success(Second(5))
    assert str_or_int_or_float_validator(5.5) == Success(Third(5.5))
    assert str_or_int_or_float_validator(True) == fail(
        {"variant 1": ["expected a string"],
         "variant 2": ["expected an integer"],
         "variant 3": ["expected a float"]})

    str_or_int_validator_named = OneOf3(
        ("name", String()),
        ("age", Integer()),
        ("alive", Float()),
    )

    assert str_or_int_validator_named(False) == fail(
        {"name": ["expected a string"],
         "age": ["expected an integer"],
         "alive": ["expected a float"]}
    )


def test_email() -> None:
    assert Email()("notanemail") == fail("expected a valid email address")
    assert Email()("a@b.com") == Success("a@b.com")

    custom_regex_validator = Email(re.compile(r"[a-z.]+@somecompany\.com"))
    assert custom_regex_validator("a.b@somecompany.com") == Success("a.b@somecompany.com")
    assert custom_regex_validator("a.b@example.com") == fail(
        "expected a valid email address")


def deserialize_and_validate_tests() -> None:
    @dataclass
    class Person:
        name: str
        age: int

    validator = Obj2(
        key("name", String()),
        key("int", Integer()),
        into=Person
    )

    assert deserialize_and_validate(validator, "") == Failure(
        {"invalid type": ["expected an object"]}
    )

    assert deserialize_and_validate(validator, "[") == Failure({
        "bad data": "invalid json"
    })

    assert deserialize_and_validate(validator,
                                    '{"name": "Bob", "age": 100}') == \
           Success(Person("Bob", 100))


def test_lazy() -> None:
    @dataclass
    class TestNonEmptyList:
        val: int
        next: Maybe['TestNonEmptyList']  # noqa: F821

    def recur_tnel() -> Obj2[int, Maybe[TestNonEmptyList], TestNonEmptyList]:
        return nel_validator

    nel_validator: Obj2[int, Maybe[TestNonEmptyList], TestNonEmptyList] = Obj2(
        key("val", Integer()),
        maybe_key("next", Lazy(recur_tnel)),
        into=TestNonEmptyList
    )

    assert nel_validator({
        "val": 5,
        "next": {
            "val": 6,
            "next": {
                "val": 7
            }
        }
    }) == Success(
        TestNonEmptyList(
            5,
            Just(
                TestNonEmptyList(
                    6,
                    Just(
                        TestNonEmptyList(
                            7,
                            Nothing
                        )
                    )
                )
            )
        )
    )


def test_unique_items() -> None:
    unique_fail = fail("all items must be unique")
    assert unique_items([1, 2, 3]) == Success([1, 2, 3])
    assert unique_items([1, 1]) == unique_fail
    assert unique_items([1, [], []]) == unique_fail
    assert unique_items([[], [1], [2]]) == Success([[], [1], [2]])
    assert unique_items([{"something": {"a": 1}}, {"something": {"a": 1}}]) == unique_fail


def test_regex_validator() -> None:
    assert RegexValidator(re.compile(r".+"))("something") == Success("something")
    assert RegexValidator(re.compile(r".+"))("") == fail("must match pattern .+")


def test_multiple_of() -> None:
    assert MultipleOf(5)(10) == Success(10)
    assert MultipleOf(5)(11) == fail("expected multiple of 5")
    assert MultipleOf(2.2)(4.40) == Success(4.40)
