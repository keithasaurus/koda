from dataclasses import dataclass
from enum import Enum

from koda.result import Failure, Success
from koda.validation import validate_and_map


def test_map_1() -> None:
    def string_thing(s: str) -> str:
        return f"valid {s}"

    assert validate_and_map(
        Failure("just returns failure"),
        string_thing, ) == Failure(('just returns failure',))

    assert validate_and_map(
        Success("hooray"),
        string_thing) == Success('valid hooray')


def test_map_2() -> None:
    @dataclass
    class Person2:
        name: str
        age: int

    assert validate_and_map(
        Failure('invalid name'),
        Failure("invalid age"),
        Person2) == Failure(('invalid name', 'invalid age'))

    assert validate_and_map(
        Success('Bob'),
        Failure("invalid age"),
        Person2) == Failure(('invalid age',))

    assert validate_and_map(
        Success("Bob"),
        Success(25),
        Person2) == Success(Person2(name='Bob', age=25))


def test_map_3() -> None:
    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int

    assert validate_and_map(
        Failure("invalid first name"),
        Failure("invalid last name"),
        Failure("invalid age"),
        Person) == Failure(
        ('invalid first name', 'invalid last name', 'invalid age'))

    assert validate_and_map(
        Failure("invalid first name"),
        Failure("invalid last name"),
        Success(25),
        Person) == Failure(('invalid first name', 'invalid last name'))

    assert validate_and_map(
        Failure("invalid first name"),
        Success("Smith"),
        Success(25),
        Person) == Failure(('invalid first name',))

    assert validate_and_map(
        Success("John"),
        Success("Doe"),
        Success(25),
        Person) == Success(Person(first_name='John',
                                  last_name='Doe',
                                  age=25))


def test_map_4() -> None:
    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int
        eye_color: str

    assert validate_and_map(
        Failure("invalid first name"),
        Failure("invalid last name"),
        Failure("invalid age"),
        Failure("invalid eye color"),
        Person) == Failure(('invalid first name',
                            'invalid last name',
                            'invalid age',
                            'invalid eye color'))

    assert validate_and_map(
        Failure("invalid first name"),
        Failure("invalid last name"),
        Success(25),
        Failure("invalid eye color"),
        Person) == Failure(
        ('invalid first name', 'invalid last name', 'invalid eye color'))

    assert validate_and_map(
        Failure("invalid first name"),
        Success("Smith"),
        Success(25),
        Failure("invalid eye color"),
        Person) == Failure(('invalid first name', 'invalid eye color'))

    assert validate_and_map(
        Success("John"),
        Success("Doe"),
        Success(25),
        Success("brown"),
        Person) == Success(Person(first_name='John',
                                  last_name='Doe',
                                  age=25,
                                  eye_color='brown'))


def test_map_5() -> None:
    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int
        eye_color: str
        can_fly: bool

    assert validate_and_map(
        Failure("invalid first name"),
        Failure("invalid last name"),
        Failure("invalid age"),
        Failure("invalid eye color"),
        Failure("invalid -- people can't fly"),
        Person) == Failure(('invalid first name',
                            'invalid last name',
                            'invalid age',
                            'invalid eye color',
                            "invalid -- people can't fly"))

    assert validate_and_map(
        Failure("invalid first name"),
        Failure("invalid last name"),
        Success(25),
        Failure("invalid eye color"),
        Success(False),
        Person) == Failure(
        ('invalid first name',
         'invalid last name',
         'invalid eye color'))

    assert validate_and_map(
        Failure("invalid first name"),
        Success("Smith"),
        Success(25),
        Failure("invalid eye color"),
        Success(False),
        Person) == Failure(('invalid first name', 'invalid eye color'))

    assert validate_and_map(
        Success("John"),
        Success("Doe"),
        Success(25),
        Success("brown"),
        Success(False),
        Person) == Success(Person(first_name='John',
                                  last_name='Doe',
                                  age=25,
                                  eye_color='brown',
                                  can_fly=False))


def test_map_6() -> None:
    class SwimmingLevel(Enum):
        BEGINNER = 1
        INTERMEDIATE = 2
        ADVANCED = 3

    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int
        eye_color: str
        can_fly: bool
        swimming_level: SwimmingLevel

    assert validate_and_map(
        Failure("invalid first name"),
        Failure("invalid last name"),
        Failure("invalid age"),
        Failure("invalid eye color"),
        Failure("invalid -- people can't fly"),
        Failure("invalid -- beginners not allowed"),
        Person) == Failure(('invalid first name',
                            'invalid last name',
                            'invalid age',
                            'invalid eye color',
                            "invalid -- people can't fly",
                            "invalid -- beginners not allowed"))

    assert validate_and_map(
        Failure("invalid first name"),
        Failure("invalid last name"),
        Success(25),
        Failure("invalid eye color"),
        Success(False),
        Success(SwimmingLevel.ADVANCED),
        Person) == Failure(
        ('invalid first name', 'invalid last name', 'invalid eye color'))

    assert validate_and_map(
        Failure("invalid first name"),
        Success("Smith"),
        Success(25),
        Failure("invalid eye color"),
        Success(False),
        Success(SwimmingLevel.ADVANCED),
        Person) == Failure(('invalid first name', 'invalid eye color'))

    assert validate_and_map(
        Success("John"),
        Success("Doe"),
        Success(25),
        Success("brown"),
        Success(False),
        Success(SwimmingLevel.ADVANCED),
        Person) == Success(Person(first_name='John',
                                  last_name='Doe',
                                  age=25,
                                  eye_color='brown',
                                  can_fly=False,
                                  swimming_level=SwimmingLevel.ADVANCED))


def test_map_7() -> None:
    class SwimmingLevel(Enum):
        BEGINNER = 1
        INTERMEDIATE = 2
        ADVANCED = 3

    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int
        eye_color: str
        can_fly: bool
        swimming_level: SwimmingLevel
        number_of_fingers: float

    assert validate_and_map(
        Failure("invalid first name"),
        Failure("invalid last name"),
        Failure("invalid age"),
        Failure("invalid eye color"),
        Failure("invalid -- people can't fly"),
        Failure("invalid -- beginners not allowed"),
        Failure("invalid number of fingers"),
        Person) == Failure(('invalid first name',
                            'invalid last name',
                            'invalid age',
                            'invalid eye color',
                            "invalid -- people can't fly",
                            "invalid -- beginners not allowed",
                            "invalid number of fingers"))

    assert validate_and_map(
        Failure("invalid first name"),
        Failure("invalid last name"),
        Success(25),
        Failure("invalid eye color"),
        Success(False),
        Success(SwimmingLevel.ADVANCED),
        Success(9.5),
        Person) == Failure(
        ('invalid first name', 'invalid last name', 'invalid eye color'))

    assert validate_and_map(
        Failure("invalid first name"),
        Success("Smith"),
        Success(25),
        Failure("invalid eye color"),
        Success(False),
        Success(SwimmingLevel.ADVANCED),
        Success(9.5),
        Person) == Failure(('invalid first name', 'invalid eye color'))

    assert validate_and_map(
        Success("John"),
        Success("Doe"),
        Success(25),
        Success("brown"),
        Success(False),
        Success(SwimmingLevel.ADVANCED),
        Success(9.5),
        Person) == Success(Person(first_name='John',
                                  last_name='Doe',
                                  age=25,
                                  eye_color='brown',
                                  can_fly=False,
                                  swimming_level=SwimmingLevel.ADVANCED,
                                  number_of_fingers=9.5))


def test_map_8() -> None:
    class SwimmingLevel(Enum):
        BEGINNER = 1
        INTERMEDIATE = 2
        ADVANCED = 3

    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int
        eye_color: str
        can_fly: bool
        swimming_level: SwimmingLevel
        number_of_fingers: float
        number_of_toes: float

    assert validate_and_map(
        Failure("invalid first name"),
        Failure("invalid last name"),
        Failure("invalid age"),
        Failure("invalid eye color"),
        Failure("invalid -- people can't fly"),
        Failure("invalid -- beginners not allowed"),
        Failure("invalid number of fingers"),
        Failure("invalid number of toes"),
        Person) == Failure(('invalid first name',
                            'invalid last name',
                            'invalid age',
                            'invalid eye color',
                            "invalid -- people can't fly",
                            "invalid -- beginners not allowed",
                            "invalid number of fingers",
                            "invalid number of toes"))

    assert validate_and_map(
        Failure("invalid first name"),
        Failure("invalid last name"),
        Success(25),
        Failure("invalid eye color"),
        Success(False),
        Success(SwimmingLevel.ADVANCED),
        Success(9.5),
        Success(3.1),
        Person) == Failure(
        ('invalid first name', 'invalid last name', 'invalid eye color'))

    assert validate_and_map(
        Failure("invalid first name"),
        Success("Smith"),
        Success(25),
        Failure("invalid eye color"),
        Success(False),
        Success(SwimmingLevel.ADVANCED),
        Success(9.5),
        Success(3.1),
        Person
    ) == Failure(('invalid first name', 'invalid eye color'))

    assert validate_and_map(
        Success("John"),
        Success("Doe"),
        Success(25),
        Success("brown"),
        Success(False),
        Success(SwimmingLevel.ADVANCED),
        Success(9.5),
        Success(3.1),
        Person
    ) == Success(Person(first_name='John',
                        last_name='Doe',
                        age=25,
                        eye_color='brown',
                        can_fly=False,
                        swimming_level=SwimmingLevel.ADVANCED,
                        number_of_fingers=9.5,
                        number_of_toes=3.1))


def test_map_9() -> None:
    class SwimmingLevel(Enum):
        BEGINNER = 1
        INTERMEDIATE = 2
        ADVANCED = 3

    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int
        eye_color: str
        can_fly: bool
        swimming_level: SwimmingLevel
        number_of_fingers: float
        number_of_toes: float
        country: str

    assert validate_and_map(
        Failure("invalid first name"),
        Failure("invalid last name"),
        Failure("invalid age"),
        Failure("invalid eye color"),
        Failure("invalid -- people can't fly"),
        Failure("invalid -- beginners not allowed"),
        Failure("invalid number of fingers"),
        Failure("invalid number of toes"),
        Failure("invalid country"),
        Person) == Failure(('invalid first name',
                            'invalid last name',
                            'invalid age',
                            'invalid eye color',
                            "invalid -- people can't fly",
                            "invalid -- beginners not allowed",
                            "invalid number of fingers",
                            "invalid number of toes",
                            "invalid country"))

    assert validate_and_map(
        Failure("invalid first name"),
        Failure("invalid last name"),
        Success(25),
        Failure("invalid eye color"),
        Success(False),
        Success(SwimmingLevel.ADVANCED),
        Success(9.5),
        Success(3.1),
        Success("USA"),
        Person) == Failure(
        ('invalid first name', 'invalid last name', 'invalid eye color'))

    assert validate_and_map(
        Failure("invalid first name"),
        Success("smith"),
        Success(25),
        Failure("invalid eye color"),
        Success(False),
        Success(SwimmingLevel.ADVANCED),
        Success(9.5),
        Success(3.1),
        Success("USA"),
        Person) == Failure(
        ('invalid first name', 'invalid eye color'))

    assert validate_and_map(
        Success("John"),
        Success("Doe"),
        Success(25),
        Success("brown"),
        Success(False),
        Success(SwimmingLevel.ADVANCED),
        Success(9.5),
        Success(3.1),
        Success("USA"),
        Person
    ) == Success(Person(first_name='John',
                        last_name='Doe',
                        age=25,
                        eye_color='brown',
                        can_fly=False,
                        swimming_level=SwimmingLevel.ADVANCED,
                        number_of_fingers=9.5,
                        number_of_toes=3.1,
                        country="USA"))


def test_map_10() -> None:
    class SwimmingLevel(Enum):
        BEGINNER = 1
        INTERMEDIATE = 2
        ADVANCED = 3

    @dataclass
    class Person:
        first_name: str
        last_name: str
        age: int
        eye_color: str
        can_fly: bool
        swimming_level: SwimmingLevel
        number_of_fingers: float
        number_of_toes: float
        country: str
        region: str

    assert validate_and_map(
        Failure("invalid first name"),
        Failure("invalid last name"),
        Failure("invalid age"),
        Failure("invalid eye color"),
        Failure("invalid -- people can't fly"),
        Failure("invalid -- beginners not allowed"),
        Failure("invalid number of fingers"),
        Failure("invalid number of toes"),
        Failure("invalid country"),
        Failure("invalid region"),
        Person) == Failure(('invalid first name',
                            'invalid last name',
                            'invalid age',
                            'invalid eye color',
                            "invalid -- people can't fly",
                            "invalid -- beginners not allowed",
                            "invalid number of fingers",
                            "invalid number of toes",
                            "invalid country",
                            "invalid region"))

    assert validate_and_map(
        Failure("invalid first name"),
        Failure("invalid last name"),
        Success(25),
        Failure("invalid eye color"),
        Success(False),
        Success(SwimmingLevel.ADVANCED),
        Success(9.5),
        Success(3.1),
        Success("USA"),
        Success("California"),
        Person) == Failure(
        ('invalid first name', 'invalid last name', 'invalid eye color'))

    assert validate_and_map(
        Failure("invalid first name"),
        Success("smith"),
        Success(25),
        Failure("invalid eye color"),
        Success(False),
        Success(SwimmingLevel.ADVANCED),
        Success(9.5),
        Success(3.1),
        Success("USA"),
        Success("California"),
        Person) == Failure(
        ('invalid first name', 'invalid eye color'))

    assert validate_and_map(
        Success("John"),
        Success("Doe"),
        Success(25),
        Success("brown"),
        Success(False),
        Success(SwimmingLevel.ADVANCED),
        Success(9.5),
        Success(3.1),
        Success("USA"),
        Success("California"),
        Person
    ) == Success(Person(first_name='John',
                        last_name='Doe',
                        age=25,
                        eye_color='brown',
                        can_fly=False,
                        swimming_level=SwimmingLevel.ADVANCED,
                        number_of_fingers=9.5,
                        number_of_toes=3.1,
                        country="USA",
                        region="California"))
