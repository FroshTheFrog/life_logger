import datetime
from config_utils import user_enter, function_maker
from data_types.time_utils import respones_to_datetime, datatime_to_string
import constants

def build_time_stamp_military_function(definition):
    """
    Builds a function that gets the data for a time_stamp_military from the user.
    Raises an error if the definition is not valid.
    str -> str -> (() -> (label: str, value: str)) or error
    """
    return function_maker(user_enter_time_stamp_military, 
                          definition, is_valid_time_stamp_military_definition, 
                          "Not a valid time_stamp_military definition: " + definition)

def is_valid_time_stamp_military_definition(definition):
    """
    Returns true if the time_stamp_military definition is valid.
    str -> bool
    """
    return True

def user_enter_time_stamp_military(definition):
    """
    Get a time_stamp_military from the user.
    Returns it along with label for the time_stamp_military.
    A time_stamp_military is a string representation of a time.
    Signature in config: time_stamp_military label
    str -> (label: str, time_stamp_military: str)
    """
    
    question = 'When did you {}?'
    valid = 'A valid response is any military time in the following respresation: Hours:Munuts'

    return user_enter(get_time_stamp_military_label,
                      user_enter_time_stamp_military_response,
                      get_time_stamp_military_from_response,
                      is_valid_time_stamp_military_response,
                      question,
                      valid,
                      definition)


def get_time_stamp_military_from_response(response):
    """
    Gets the value from a valid time_stamp_military response.
    str -> str
    """
    time = respones_to_datetime(response, constants.DATETIME_FORMATE_MILITARY)
    return datatime_to_string(time, constants.DATETIME_FORMATE_MILITARY)
    
def is_valid_time_stamp_military_response(response):
    """
    Returns true if a time_stamp_military response is valid.
    str -> bool
    """
    try:
        respones_to_datetime(response, constants.DATETIME_FORMATE_MILITARY)
        return True
    except ValueError:
        return False

def user_enter_time_stamp_military_response():
    """
    Prompts the user to enter a time_stamp_military response.
    nothing -> str
    """
    return input('Military Time: ')
    
def get_time_stamp_military_label(definition):
    """
    Given a valid time_stamp_military definition, returns its label.
    str -> str
    """
    return definition