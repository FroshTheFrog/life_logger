from config_utils import user_enter, function_maker

def build_did_do_function(definition):
    """
    Builds a function that gets the data for a did_do from the user.
    Raises an error if the definition is not valid.
    str -> (() -> (label: str, value: bool)) or error
    """
    return function_maker(user_enter_did_do, 
                          definition, is_valid_did_do_definition, 
                          "Not a valid did_do definition: " + definition)

def is_valid_did_do_definition(definition):
    """
    Returns true if the did_do definition is valid.
    str -> bool
    """
    return True 

def user_enter_did_do(definition):
    """
    Gets a did_do from the user.
    Returns it along with label for the value.
    A did_do is a bool.
    Signature in config: did_do label
    str -> (label: str, value: bool)
    """

    question = 'Did you {}?'

    return user_enter(get_did_do_label, 
                      user_enter_boolean_response, 
                      get_bool_from_response,
                      is_valid_boolean_response,
                      question,
                      VALID_BOOL_RESPONSE,
                      definition)


def user_enter_boolean_response():
    """
    Prompts the user to enter a boolean response and returns its value in lower case.
    nothing -> str
    """
    return input('(y/n) ').lower()

def get_did_do_label(definition):
    """
    Given a valid did_do definition, returns its label.
    str -> str
    """
    return definition

def get_bool_from_response(response):
    """
    Given a valid bool response, returns the response in boolean form.
    str -> bool
    """
    return response == 'y'

def is_valid_boolean_response(response):
    """
    Returns true if a boolean response is valid.
    str -> bool
    """
    return response == 'n' or response == 'y'

VALID_BOOL_RESPONSE = 'A valid response is eather "y" for True or "n" for False.'