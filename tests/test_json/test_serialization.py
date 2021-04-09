from json import JSONDecodeError

from koda.json.serialization import json_to_str, str_to_json
from koda.result import Failure, Success

from ..utils import assert_same_error_type_with_same_message


def test_str_to_json() -> None:
    assert str_to_json('''{"a": 5}''') == Success({"a": 5})

    assert_same_error_type_with_same_message(
        str_to_json('''{"a":}'''),
        Failure(
            JSONDecodeError('Expecting value',
                            '{"a":}',
                            pos=5)
        )
    )


def test_str_to_json_deserialized_type() -> None:
    assert str_to_json('''{"a": 5}''') == Success({"a": 5})

    assert_same_error_type_with_same_message(
        str_to_json('''{"a":}'''),
        Failure(
            JSONDecodeError('Expecting value',
                            '{"a":}',
                            pos=5)
        )
    )


def test_json_to_str() -> None:
    assert json_to_str({"hello": "ok"}) == '''{"hello": "ok"}'''
