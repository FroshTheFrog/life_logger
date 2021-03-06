from data_types.did_do import build_did_do_function
from data_types.key_event import build_key_event_function
from data_types.note import build_note_function
from data_types.state_change import build_state_change_function
from data_types.time import build_time_function
from data_types.range import build_range_function
from data_types.floating_point import build_floating_point_function
from data_types.integer import build_integer_function
from data_types.time_stamp_military import build_time_stamp_military_function
from data_types.time_stamp_normal import build_time_stamp_normal_function
from data_types.if_yes import build_if_yes_function

COMMENT_OUT_STRING = '//'

LINE = '------------------------------------------------------'

MULTILINE_COMMENT_START = '/*'

MULTILINE_COMMENT_END = '*/'

DEFAULT_CONFIG_PATH = 'config.txt'

SAVE_DATA_PATH = 'saves\\'

SAVED_DATA_NAME_TAG = 'save';

DATETIME_FORMATE_NORMAL = '%I:%M %p'

DATETIME_FORMATE_MILITARY = '%H:%M'

DATETIME_FORMATE_JUST_DATE = '%x'

QUESTION_DENOTE = '"'

WHEN_NOTHING_TO_lOG = ''

"""
A map of type names to input functions.
map of str to (str -> (() -> (label: str, value: any)))
"""
TYPE_MAP = {
        'range' : build_range_function,
        'time' : build_time_function,
        'did_do' : build_did_do_function,
        'note' : build_note_function,
        'key_event' : build_key_event_function,
        'state_change' : build_state_change_function,
        'floating_point' : build_floating_point_function,
        'integer' : build_integer_function,
        'time_stamp_military' : build_time_stamp_military_function,
        'time_stamp_normal' : build_time_stamp_normal_function
        }

"""
A map of complex types to input functions.
A complex type is defined as a type that references the TYPE_MAP in its logic.
This is used so that there are no circular dependencies.
map of str to (str -> (() -> (label: str, value: any)))
"""
COMPLEX_TYPE_MAP = {
        'if_yes' : build_if_yes_function
        }