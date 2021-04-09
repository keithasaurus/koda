"""
This file is meant to be run as a script and just outputs
definitions of Obj<N> classes
"""

from typing import List


def get_type_vars(var_count: int) -> List[str]:
    return [chr(j + 65) for j in range(var_count)]


def generate_code(obj_count: int) -> str:
    obj_classes = []

    for i in range(1, obj_count + 1):
        type_vars = get_type_vars(i)
        predicate_type_vars = ", ".join(type_vars)

        fields_init = ",\n                 ".join([
            f"field{j + 1}: KeyValidator[{type_var}]"
            for j, type_var in enumerate(type_vars)
        ])

        fields_init_tuple = ",\n                       ".join(
            [f"field{j + 1}" for j in range(i)]
        )

        key_validations = "\n                ".join([
            f"_validate_with_key(self.fields[{j}], result.val),"
            for j in range(i)
        ])

        obj_classes.append(f"""
class Obj{i}(Generic[{predicate_type_vars}, Ret],
           TransformableValidator[Any, Ret, Jsonable]):
    def __init__(self,
                 {fields_init},
                 *,
                 into: Callable[[{predicate_type_vars}], Ret],
                 validate_object: Optional[Callable[[Ret], Result[Ret, Jsonable]]] = None
                 ) -> None:
        self.fields = ({fields_init_tuple},)
        self.into = into
        self.validate_object = validate_object

    def __call__(self, data: Any) -> Result[Ret, Jsonable]:
        # ok, not sure why this works, but {{f.key for f in self.fields}} doesn't
        result = _dict_without_extra_keys({{self.fields[x][0]
                                           for x in range(len(self.fields))}},
                                           data)

        if isinstance(result, Failure):
            return result
        else:
            result_1 = validate_and_map(
                {key_validations}
                self.into
            )
            return _flat_map_same_type_if_not_none(
                self.validate_object,
                result_1.map_failure(_tuples_to_jsonable_dict))
                """)

    obj_overloads = []

    for i in range(1, obj_count + 1):
        type_vars = get_type_vars(i)
        field_validators = "\n        ".join([
            f"f{j + 1}: KeyValidator[{tv}]," for j, tv
            in enumerate(type_vars)
        ])

        type_vars_joined = ", ".join(type_vars)

        obj_overloads.append(f"""
@overload
def obj(
        {field_validators}
        *,
        into:  Callable[[{type_vars_joined}], Ret]
) -> Obj{i}[{type_vars_joined}, Ret]:
    ...

""")

    return "\n\n".join(obj_classes)


if __name__ == "__main__":
    print(generate_code(10))
