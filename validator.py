import json
from collections import OrderedDict
import re
from typing import List, Dict

import errors_codes


class ValidationError:

    def __init__(self, code, params):
        self.__code = code
        self.__params = params

    def code(self):
        return self.__code

    def params(self):
        return self.__params

    def toMap(self):
        return {'code': self.code(), 'params': self.params()}


class WrongFieldError(ValidationError):
    def __init__(self, code, field_name):
        super().__init__(code, {'field_name': field_name})


class FieldValidator:

    __field_name = None
    __min_len = 1
    __max_len = 255
    __required = False
    __email = False
    __values = None
    __type = str

    def __init__(self, __field_name: str):
        self.__field_name = __field_name.strip()

    def field_name(self):
        return self.__field_name

    def is_required(self):
        return self.__required

    def min_len(self, __min_len: int):
        self.__min_len = __min_len
        return self

    def max_len(self, __max_len: int):
        self.__max_len = __max_len
        return self

    def required(self):
        self.__required = True
        return self

    def email(self):
        self.__email = True
        return self

    def values(self, *__values):
        self.__values = list(__values)
        return self

    def string(self):
        self.__type = str
        return self

    def integer(self):
        self.__type = int
        return self

    def boolean(self):
        self.__type = bool
        return self

    def validate(self, field_value: str):
        if self.is_required():
            if field_value is None:
                return WrongFieldError(errors_codes.missing_field, self.__field_name)
            if len(field_value) == 0:
                return ValidationError(errors_codes.empty_field, {'field_name': self.__field_name})

        if len(field_value) < self.__min_len:
            return WrongFieldError(errors_codes.field_too_short, self.__field_name)

        if len(field_value) > self.__max_len:
            return WrongFieldError(errors_codes.field_too_long, self.__field_name)

        if self.__email and not re.match("[a-z0-9\-\.]+@[a-z0-9\-\.]+\.[a-z]+", field_value, re.IGNORECASE):
            return WrongFieldError(errors_codes.wrong_email, self.__field_name)

        if self.__type == bool:
            if field_value == '0' or field_value == 'false':
                field_value = False
            elif field_value == '1' or field_value == 'true':
                field_value = True
            else:
                return WrongFieldError(errors_codes.wrong_field_type, self.__field_name)

        if self.__values is not None and field_value not in self.__values:
            return WrongFieldError(errors_codes.wrong_field_type, self.__field_name)

        return None


def validate(params: Dict[str, str], validators: List[FieldValidator]):
    errors = []
    values = []
    if params is None:
        params = {}
    for validator in validators:
        field_name = validator.field_name()
        field_value = None
        if field_name in params:
            field_value = params[field_name]
        error = validator.validate(field_value)
        if error is not None:
            errors.append(error.toMap())
        values.append(field_value)
    return values, errors
