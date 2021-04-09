# A sample schema
schema = {
    "type": "object",
    "required": [
        "name"
    ],
    "properties": {
        "name": {
            "type": "string"
        },
        "age": {
            "type": "integer",
            "format": "int32",
            "minimum": 0,
            "nullable": True,
        },
        "birth-date": {
            "type": "string",
            "format": "date",
        }
    },
    "additionalProperties": False,
}

# If no exception is raised by validate(), the instance is valid.
# validate({"name": "John", "age": 23}, schema)

# validate({"name": "John", "city": "London"}, schema)
