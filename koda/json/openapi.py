from typing import Any, Dict, List, NoReturn, Union

import koda.json.validation as v
from koda.json.serialization import JsonSerializable
from koda.validation import PredicateValidator, TransformableValidator


def unhandled_type(obj: Any) -> NoReturn:
    raise TypeError(f"type {type(obj)} not handled")


def string_schema(schema_name: str,
                  validator: v.String) -> Dict[str, JsonSerializable]:
    ret: Dict[str, JsonSerializable] = {
        'type': 'string'
    }
    for sub_validator in validator.validators:
        ret.update(generate_schema_base(schema_name, sub_validator))

    return ret


def integer_schema(schema_name: str,
                   validator: v.Integer) -> Dict[str, JsonSerializable]:
    ret: Dict[str, JsonSerializable] = {
        "type": "integer"
    }
    for sub_validator in validator.validators:
        ret.update(generate_schema_base(schema_name, sub_validator))
    return ret


def float_schema(schema_name: str,
                 validator: v.Float) -> Dict[str, JsonSerializable]:
    ret: Dict[str, JsonSerializable] = {
        "type": "number"
    }
    for sub_validator in validator.validators:
        ret.update(generate_schema_base(schema_name, sub_validator))
    return ret


def boolean_schema(schema_name: str,
                   validator: v.Boolean) -> Dict[str, JsonSerializable]:
    ret: Dict[str, JsonSerializable] = {
        "type": "boolean"
    }
    for sub_validator in validator.validators:
        ret.update(generate_schema_base(schema_name, sub_validator))
    return ret


def array_of_schema(schema_name: str,
                    validator: v.ArrayOf[Any]) -> Dict[str, JsonSerializable]:
    ret: Dict[str, JsonSerializable] = {
        "type": "array",
        "items": generate_schema_base(schema_name, validator.item_validator)
    }

    for sub_validator in validator.list_validators:
        ret.update(generate_schema_base(schema_name, sub_validator))

    return ret


def obj_schema(schema_name: str,
               obj: Union[v.Obj1[Any, Any],
                          v.Obj2[Any, Any, Any],
                          v.Obj3[Any, Any, Any, Any],
                          v.Obj4[Any, Any, Any, Any, Any],
                          v.Obj5[Any, Any, Any, Any, Any, Any],
                          v.Obj6[Any, Any, Any, Any, Any, Any, Any],
                          v.Obj7[Any, Any, Any, Any, Any, Any, Any, Any],
                          v.Obj8[Any, Any, Any, Any, Any, Any, Any, Any, Any],
                          v.Obj9[Any, Any, Any, Any, Any, Any, Any, Any, Any, Any],
                          v.Obj10[Any, Any, Any, Any, Any, Any, Any, Any, Any, Any, Any]]
               ) -> Dict[str, JsonSerializable]:
    required: List[str] = []
    properties: Dict[str, JsonSerializable] = {}
    for label, field in obj.fields:
        if isinstance(field, v.RequiredField):
            required.append(label)
        if isinstance(field, (v.RequiredField, v.MaybeField)):
            properties[label] = generate_schema_base(schema_name,
                                                     field.validator)
        else:
            # TODO: is this correct? has the result of this for "some-label":
            #   {"properties: {"some-label": {}, ...}}
            properties[label] = {}

    return {
        'type': 'object',
        'additionalProperties': False,
        # ignoring because of a mypy bug where it doesn't understnad List[str] can be
        #   JsonSerializable; as of mypy 0.812
        'required': required,  # type: ignore
        'properties': properties
    }


def map_of_schema(schema_name: str,
                  obj: v.MapOf[Any, Any]) -> Dict[str, JsonSerializable]:
    ret: Dict[str, JsonSerializable] = {
        "type": "object",
        "additionalProperties": generate_schema_base(schema_name,
                                                     obj.value_validator)
    }

    for dict_validator in obj.dict_validators:
        ret.update(generate_schema_base(schema_name, dict_validator))

    return ret


def generate_schema_predicate(
        validator: PredicateValidator[Any, Any]) -> Dict[str, JsonSerializable]:
    # strings
    if isinstance(validator, v.Email):
        return {'format': 'email'}
    elif isinstance(validator, v.MaxLength):
        return {'maxLength': validator.length}
    elif isinstance(validator, v.MinLength):
        return {'minLength': validator.length}
    elif isinstance(validator, v.Enum):
        return {'enum': list(sorted(validator.choices))}
    elif isinstance(validator, v.NotBlank):
        return {"pattern": r"^(?!\s*$).+"}
    elif isinstance(validator, v.RegexValidator):
        return {"pattern": validator.pattern.pattern}
    # enums
    elif isinstance(validator, v.Enum):
        return {"enum": list(sorted(validator.choices))}
    # numbers
    elif isinstance(validator, v.Minimum):
        return {"minimum": validator.minimum,
                "exclusiveMinimum": validator.exclusive_minimum}
    elif isinstance(validator, v.Maximum):
        return {"maximum": validator.maximum,
                "exclusiveMaximum": validator.exclusive_maximum}
    # objects
    elif isinstance(validator, v.MinProperties):
        return {"minProperties": validator.size}
    elif isinstance(validator, v.MaxProperties):
        return {"maxProperties": validator.size}
    # arrays
    elif isinstance(validator, v.MinItems):
        return {"minItems": validator.length}
    elif isinstance(validator, v.MaxItems):
        return {"maxItems": validator.length}
    elif isinstance(validator, v.UniqueItems):
        return {"uniqueItems": True}
    else:
        unhandled_type(validator)


def generate_schema_transformable(
        schema_name: str,
        obj: TransformableValidator[Any, Any, Any]) -> Dict[str, JsonSerializable]:
    # caution, mutation below!
    if isinstance(obj, v.Boolean):
        return boolean_schema(schema_name, obj)
    if isinstance(obj, v.String):
        return string_schema(schema_name, obj)
    elif isinstance(obj, v.Integer):
        return integer_schema(schema_name, obj)
    elif isinstance(obj, v.Float):
        return float_schema(schema_name, obj)
    elif isinstance(obj, v.Nullable):
        maybe_val_ret = generate_schema_base(schema_name, obj.validator)
        assert isinstance(maybe_val_ret, dict)
        maybe_val_ret['nullable'] = True
        return maybe_val_ret
    elif isinstance(obj, v.MapOf):
        return map_of_schema(schema_name, obj)
    elif isinstance(obj, (v.Obj1,
                          v.Obj2,
                          v.Obj3,
                          v.Obj4,
                          v.Obj5,
                          v.Obj6,
                          v.Obj7,
                          v.Obj8,
                          v.Obj9,
                          v.Obj10)):
        return obj_schema(schema_name, obj)
    elif isinstance(obj, v.ArrayOf):
        return array_of_schema(schema_name, obj)
    elif isinstance(obj, v.Lazy):
        if obj.recurrent:
            return {"$ref": f"#/components/schemas/{schema_name}"}
        else:
            return generate_schema_base(schema_name, obj.validator)
    elif isinstance(obj, v.OneOf2):
        return {
            "oneOf": [generate_schema_base(schema_name, s) for s in [obj.variant_one,
                                                                     obj.variant_two]]
        }
    elif isinstance(obj, v.OneOf3):
        return {
            "oneOf": [generate_schema_base(schema_name, s)
                      for s in [obj.variant_one,
                                obj.variant_two,
                                obj.variant_three]]
        }
    elif isinstance(obj, v.Tuple2):
        return {
            "description":
                'a 2-tuple; schemas for slots are listed in order in "items" > "anyOf"',
            "type": "array",
            "maxItems": 2,
            "items": {
                "anyOf": [generate_schema_base(schema_name, s)
                          for s in [obj.slot1_validator,
                                    obj.slot2_validator]]
            }
        }
    elif isinstance(obj, v.Tuple3):
        return {
            "description":
                'a 3-tuple; schemas for slots are listed in order in "items" > "anyOf"',
            "type": "array",
            "maxItems": 3,
            "items": {
                "anyOf": [generate_schema_base(schema_name, s)
                          for s in [obj.slot1_validator,
                                    obj.slot2_validator,
                                    obj.slot3_validator]]
            }
        }
    else:
        unhandled_type(obj)


def generate_schema_base(schema_name: str,
                         obj: Any) -> Dict[str, JsonSerializable]:
    if isinstance(obj, TransformableValidator):
        return generate_schema_transformable(schema_name, obj)
    elif isinstance(obj, PredicateValidator):
        return generate_schema_predicate(obj)
    else:
        unhandled_type(obj)


def generate_schema(schema_name: str,
                    obj: Any) -> Dict[str, JsonSerializable]:
    return {schema_name: generate_schema_base(schema_name, obj)}
