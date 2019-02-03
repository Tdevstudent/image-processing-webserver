import config
import string
import random
import json
import os.path


def filename_get_random():
    """ returns random file name of length specified in config
    """
    filename = ""
    for _ in range(config.filename_length):
        char = random.SystemRandom().choice(
            string.ascii_uppercase + string.ascii_lowercase + string.digits)
        filename += char
    return filename


def filename_is_valid(filename):
    """
    checks whether a filename is valid

    :param image_name filename to be checked

    :returns (is_valid, error)
    :param is_valid True if filename is valid, False otherwise
    :param error String with errormessage, None if is_valid equals True
    """
    error = None
    is_valid = True

    if (not isinstance(filename, str)):
        error = "invalid type, expected: string"
        is_valid = False
        return is_valid, error

    try:
        name, ext = os.path.splitext(filename)
    except Exception:
        error = "unable to split extension"
        is_valid = False
        return is_valid, error

    if ext not in config.allowed_filetypes:
        error = "illegal file extension:" + ext
        is_valid = False
        return is_valid, error

    if (len(name) != config.filename_length):
        error = "incorrect name length"
        is_valid = False
        return is_valid, error

    for c in name:
        if c not in (string.ascii_lowercase + string.ascii_uppercase + string.digits):
            error = "illegal character"
            is_valid = False
            break

    return is_valid, error


def json_load_from_request(request):
    """
    tries to load json from a request object

    :param request a Flask request object

    :returns (valid_json, json, errors)
    :param valid_json True if json is valid, False otherwise
    :param json json object (dict), None if valid_json is False
    :param errors List of error messages
    """
    errors = []
    if request.json is None:
        errors.append("JSON not found")
        return False, None, errors
    try:
        if isinstance(request.json, dict):
            return True, json.loads(json.dumps(request.json)), []
        return True, json.loads(request.json), []
    except Exception:
        errors.append("Unable to load JSON")
        return False, None, errors


def json_has_fields(json, fields):
    """
    checks if fields are present in the json
    an error message is returned for each field not present

    :param json a JSON dict
    :param fields List of field names

    :returns (has_fields, errors)
    :param has_fields True if all fields are present in the json, False otherwise
    :param errors List of error messages
    """
    errors = []
    has_fields = True
    for field_name in fields:
        if field_name not in json:
            errors.append(field_name + " field missing")
            has_fields = False
    return has_fields, errors
