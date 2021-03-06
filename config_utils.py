import constants
from formatting_utils import quote_pad

# A definition is the text following space after the type name.

def user_enter(get_label,
                user_enter_response, 
                get_data_from_response,
                is_valid_data,
                opening_question_text, 
                valid_respones_text,
                definition):
    """
    Asks the user to enter data to be logged.
    Returns the data along with label for the data.
    Parameters
    ----------
    get_label : str -> str
        gets the data's label from the definition.
    user_enter_response : nothing -> str
        Prompts the user to enter a data response.
    is_valid_data : str -> bool
        Returns true if the data is valid.
    opening_question_text : str
        The text for the question prompted the user the user somthing.
        This would come with a spot: {} for the data label.
    valid_respones_text : str
        The text that define a valid response.
    definition : str
        The definition for the data.
    ----------
    str -> (label: str, data: any)
    """

    label = get_label(definition)
    
    print(opening_question_text.format(label))
    response = user_enter_response()

    while not is_valid_data(response):
        print()
        print('Please enter a valid response.')
        print(valid_respones_text)
        response = user_enter_response()

    value = get_data_from_response(response)

    return (label, value)

def config_to_functions(config):
    """
    Takes in the data for a config and returns a list of functions to call the meet it's criteria.
    list of str -> list of (none -> (str, any))
    """

    functions = []
    
    in_multiline_comment = False

    for line in config:
        line = remove_new_lines(line)
        
        in_multiline_comment = in_multiline_comment or line_starts_multiline_comment_start(line)
        multiline_comment_end = line_starts_multiline_comment_end(line)
        
        if not in_multiline_comment and multiline_comment_end:
            message = 'Multiline comment end: ' + constants.MULTILINE_COMMENT_END
            message += ' must inclose a comment.'
            raise Exception(message)
        
        if multiline_comment_end:
            in_multiline_comment = False

        # Skip necessary lines.
        if (is_line_commented(line) or 
            is_empty_line(line) or 
            in_multiline_comment or 
            multiline_comment_end):
            continue

        check_config_line(line)

        command_type = get_command_type(line)
        if not is_type(command_type) and not is_complex_type(command_type):
            on_not_valid_type(command_type)

        definition = get_command_definition(line)

        # Have to do binding because Python is retarded: https://stackoverflow.com/questions/58667027/string-values-are-passed-in-as-reference-to-a-python-lambda-for-some-reason?noredirect=1#comment103636999_58667027
        functions.append(build_input_func(
            any_type_to_input_functions(command_type, definition), 
            command_type))

    if in_multiline_comment:
        message = 'Multiline comment start: ' + constants.MULTILINE_COMMENT_START
        message += ' must be inclosed with: ' + constants.MULTILINE_COMMENT_END
        raise Exception(message)

    return functions

def build_input_func(input_func, data_type):
    """
    Returns a fully construced user input function when given the input function and the data type type it returns.
    (() -> (any, str)), str -> (() -> (any, str))
    """
    return lambda: append_command_type(input_func, data_type)

def append_command_type(user_enter, command_type):
    """
    Returns a the output of a user enter function function and  appends the command type to the label of the data.
    (() -> (any, str)), str -> (any, str)
    """
    value = user_enter()
    return (command_type + ' ' + value[0], value[1])

def is_empty_line(line):
    """
    Returns true if a given line is empty.
    str -> bool
    """
    return len(line) == 0

def get_command_type(line):
    """
    Returns the command type.
    str -> str
    """
    line = line.split(' ', 1)
    return line[0]

def get_command_definition(line):
    """
    Returns the command definition.
    str -> str
    """
    line = line.split(' ', 1)
    return line[1]

def string_starts_with(string, start):
    """
    Returns true if a string starts with a value.
    str -> bool
    """
    length = len(start)
    return len(string) >= length and string[0:length] == start

def is_line_commented(line):
    """
    Returns true if the given line was commented out.
    str -> bool
    """
    return string_starts_with(line, constants.COMMENT_OUT_STRING)

def line_starts_multiline_comment_start(line):
    """
    Returns true if the given line starts with a multiline comment start.
    str -> bool
    """
    return string_starts_with(line, constants.MULTILINE_COMMENT_START)

def line_starts_multiline_comment_end(line):
    """
    Returns true if the given line starts with a multiline commentend .
    str -> bool
    """
    return string_starts_with(line, constants.MULTILINE_COMMENT_END)

def function_maker(input_func, perameter, perameter_verifier, exception_message):
    """
    Checks that a given peramater is valid. If so return
    a function and it's perameter returned as function object. Else, raise an exception.
    (str -> anything), str, (str -> bool), str -> (none -> anything)
    """
    if perameter_verifier(perameter):
        return lambda: input_func(perameter)
    
    raise Exception(exception_message)

def any_type_to_input_functions(type, definition):
    """
    Returns the function returned by the input function of any given type. 
    string, string -> (str -> anything)
    """
    if is_type(type):
        return type_to_input_functions(type, definition)
    return complex_type_to_input_functions(type, definition)

def type_to_input_functions(type, definition):
    """
    Returns the function returned by the input function of a given type. 
    string, string -> (str -> anything)
    """
    return constants.TYPE_MAP[type](definition)

def complex_type_to_input_functions(type, definition):
    """
    Returns the function returned by the input function of a given complex type. 
    string, string -> (str -> anything)
    """
    return constants.COMPLEX_TYPE_MAP[type](definition)

def is_type(config_type):
    """
    Returns true if a given type is valid.
    str -> bool
    """
    return config_type in constants.TYPE_MAP

def is_complex_type(config_type):
    """
    Returns true if a given type is valid.
    str -> bool
    """
    return config_type in constants.COMPLEX_TYPE_MAP

def on_not_valid_type(type):
    """
    Raises the exception that occurs when a none valid type is parsed.
    str -> exception
    """
    raise Exception(quote_pad(type) + ' is not a valid type')

def check_config_line(line):
    """
    Checks that a given line in the config is valid.
    If not, throw an exception.
    str -> none or error
    """
    if len(line.split(' ', 1)) == 1:
        raise Exception('Invalid config line: ' + quote_pad(line))

def remove_new_lines(string):
    """
    Returns a given string with its newlines striped from it.
    str -> str
    """
    return string.strip('\n')