def validate_string_param(value, name):
    if not value:
        raise ValueError("The {0} parameter is required".format(name))

    if not isinstance(value, str):
        raise TypeError("The {0} parameter must be of type str".format(name))

def validate_boolean_param(value, name):
    if not value:
        raise ValueError("The {0} parameter is required".format(name))

    if not isinstance(value, bool):
        raise TypeError("The {0} parameter must be of type bool".format(name))