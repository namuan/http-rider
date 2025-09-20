import ast
import random
import re
import string

from httprider.core.faker_config import fake
from httprider.core.util_functions import *

# Internal function arguments must be one or more of
# \d (digit) \w (word) \" (") \* (*) \# (#) \- (-) \, (,) \s (space) \= \: (base64)
internal_func_rgx = re.compile(r"\$\{(\w+)\(([\d\w\"\*\#\-\,\.\/\=\s\:]*)\)\}", re.MULTILINE | re.IGNORECASE)

address_attributes_map = {
    "country": fake.country,
    "address": fake.address,
    "secondary": fake.secondary_address,
    "street": fake.street_address,
    "city": fake.city,
    "zipcode": fake.zipcode,
    "state": fake.state,
}


def random_address(args):
    attribute = args
    return address_attributes_map.get(attribute.lower())()


person_attributes_map = {
    "male": {
        "prefix": fake.prefix_male,
        "first_name": fake.first_name_male,
        "last_name": fake.last_name_male,
        "full_name": fake.name_male,
        "suffix": fake.suffix_male,
    },
    "female": {
        "prefix": fake.prefix_female,
        "first_name": fake.first_name_female,
        "last_name": fake.last_name_female,
        "full_name": fake.name_female,
        "suffix": fake.suffix_female,
    },
}


def random_person(args):
    attribute, gender = args
    return person_attributes_map.get(gender.lower()).get(attribute)()


# ruff: noqa: S311
def custom_string_generator(args):
    pattern, upper_case = args

    def subs(char_in_pattern):
        if char_in_pattern == "*":
            if upper_case:
                return random.choice(string.ascii_uppercase)
            else:
                return random.choice(string.ascii_lowercase)
        if char_in_pattern == "#":
            return random.choice(string.digits)
        return char_in_pattern

    return "".join([subs(c) for c in pattern])


def random_uuid():
    return fake.uuid4()


def random_string_generator(args):
    chars, letters, digits, *specials = args
    specials = specials or False

    selection = ""
    if letters:
        selection += string.ascii_letters
    if digits:
        selection += string.digits
    if specials:
        selection += string.punctuation

    if not selection:
        selection = string.digits + string.ascii_letters + string.punctuation

    return "".join(random.choice(selection) for i in range(int(chars)))


def utils_func_applicator(args):
    func_name, params = args
    return utility_func_map.get(func_name)(params)


def noop(args):
    return f"Invalid function called with {args}"


def call_generator_func(func_name, parsed_args):
    args = None if not parsed_args else ast.literal_eval(parsed_args)
    m = {
        "random": random_string_generator,
        "uuid": random_uuid,
        "custom": custom_string_generator,
        "person": random_person,
        "address": random_address,
        "file": file_func_generator,
        "utils": utils_func_applicator,
    }

    generator_function = m.get(func_name)
    if generator_function and args:
        return generator_function(args)
    elif generator_function and not args:
        return generator_function()
    else:
        return noop(args)


# Accepts a regex match object which should have matched the regex for internal_func_rgx
# So the task for this method is to extract the function name and any arguments
# Then it calls gen_map to call the function (with args) and return the result back
# The result is then substituted in place of the function in the original string (templated_string)
# for eg. ${random(32, True, True)} will be substituted with the random value generated
def return_func_result(s):
    return call_generator_func(s.group(1), s.group(2))


def file_func_generator(args, wrap_in_quotes=False):
    if wrap_in_quotes:
        return f'${{file("{args}")}}'
    else:
        return f"${{file({args})}}"


def is_file_function(func_value):
    return internal_func_rgx.search(func_value)
