import sys
import constants


'''
Event types:

Will need:
- Config file for things to track
- A way to visualize data
- Some premade analisis using ML and data science algo
- A way to log data in the consol

Data def:
    - value(a,b) (integer from 0 to 10 inclusive)
    - time (number in hours)
    - did_do ("y" or "n")
    - note (string)
    - keyevent (string)
    - stateChange: (string)
        When my current living state changes. This data will be carried to every new log unless
        specified otherwise

My config:
// emotions
    value (0,3) Energy
    value (0,3) Sociability
    value (0,3) Melancholy
    value (0,3) Self Assurance
    value (0,3) Stress
    value (0,3) Aggression
    value (0,3) Longing
    value (0,3) Contentness
    value (0,3) Focus
    value (0,3) Disgust
    value (0,3) Passion For Life
    value (0,3) Appreciation

// Activity
    did_do Meditate
    did_do Exercised
    did_do Got a Good Nights Sleep
    did_do Read
    did_do Worked on Side Project
    value (0,3) Ate low carbs
    value (0,3) Amount of Food Eaten
    value (0,3) socialized
    value (0,3) walked around white lost in thought
    value (0,3) did school work

// Notes
    note things I learned
    note notworthy stuff
    keyevent key events
    sateChange housing
    sateChange school, work, ect...

output:
xml
    
'''
# TODO: CHECK VALIDITY OF DEFINITIONS


# A definition is the text following space after the type name.

# Get a value from the user.
# Returns it along with label for the value.
# A value is a int from a to b inclusive.
# Signature in config: value (a,b) label
# str -> (label: str, value: int)
def user_enter_value(definition):
    label = get_value_label(definition)
    range = get_value_range(definition)
    a = range[0]
    b = range[1]

    inclusive_exclusive = 'From a scale from {} inclusive to {} exclusive, '.format(a,b)
    question = inclusive_exclusive + 'how would you rate your {}'.format(label)
    print(question)
    response = user_enter_value_response()

    while (not is_valid_value(response, a, b)):
        print('Please enter a valid response')
        print('A valid response is a integer ' + inclusive_exclusive.lower())
        response = user_enter_value_response()

    value = get_value_from_response(response)

    return (label, value)

# Prompts the user to enter a value response.
# nothing -> str
def user_enter_value_response():
    return input('Value: ')

# Given a value definition, returns its label.
# str -> str
def get_value_label(definition):
    return definition.split(' ')[1]

# Given a value definition, returns its range.
# str -> (int, int)
def get_value_range(definition):
    range = definition.split(' ')[0]
    values = range.split(',')
    a = values[0][1:]
    b = values[1][:-1]
    return (int(a), int(b))

# Given a user response and a range of numbers,
# Returns if the response in a int and that in falls in range of [a, b)
# str, number, number -> bool
def is_valid_value(response, a, b):
    if response.isdigit():
        value = get_value_from_response(response)
        return value >= a and value < b
    return False

# Returns true if a boolean response is valid.
# str -> int
def get_value_from_response(response):
    return int(response)

# Get a time from the user.
# Returns it along with label for the value.
# A time is a float.
# Signature in config: time label
# str -> (label: str, value: float)
def user_enter_time(definition):
    print("time " + definition)

# Gets a did_do from the user.
# Returns it along with label for the value.
# A did_do is a bool.
# Signature in config: did_do label
# str -> (label: str, value: bool)
def user_enter_did_do(definition):

    label = get_did_do_label(definition)

    print('Did you {}?'.format(label))
    response = user_enter_boolean_response()

    while (not is_valid_boolean_response(response)):
        print('Please enter a valid response')
        print('A valid response is eather "y" for True or "n" for False.')
        response = user_enter_boolean_response()

    bool_response = get_bool_from_response(response)

    return (label, bool_response)

# Prompts the user to enter a boolean response and returns its value in lower case.
# nothing -> str
def user_enter_boolean_response():
    return input('(y/n)').lower()
    
# Given a valid did do, returns its label.
# str -> str
def get_did_do_label(definition):
    return definition

# Given a valid bool response, returns the response in boolean form.
# str -> bool
def get_bool_from_response(response):
    return response == 'y'

# Returns true if a boolean response is valid.
# str -> bool
def is_valid_boolean_response(response):
    return response == 'n' or response == 'y'

# Gets a note from the user.
# Returns it along with label for the value.
# A note is a str.
# Signature in config: note label
# str -> (label: str, value: str)
def user_enter_note(definition):
    print("get note " + definition)

# Gets a key_event from the user.
# Returns it along with label for the value.
# A key_event is a str.
# Signature in config: key_event label
# str -> (label: str, value: str)
def user_enter_key_event(definition):
    print("key event " + definition)

# Gets a state_change from the user.
# Returns it along with label for the value.
# A state_change is a str.
# Signature in config: state_change label
# str -> (label: str, value: str)
def user_enter_state_change(definition):
    print("state change " + definition)

# Takes in the data for a config and returns a list of functions to call the meet it's criteria.
# list of str -> list of (none -> str)
def config_to_functions(config):
    type_to_input_functions = get_type_map()

    functions = []

    for line in config:

        # Skip the lines that are commented out.
        if (is_line_commented(line)):
            continue

        check_config_line(line)

        type = get_command_type(line)
        check_type(type)

        definition = get_command_definition(line)

        # Have to do binding because Python is retarded: https://stackoverflow.com/questions/58667027/string-values-are-passed-in-as-reference-to-a-python-lambda-for-some-reason?noredirect=1#comment103636999_58667027
        functions.append(function_maker(type_to_input_functions[type], definition))

    return functions

# Returns the command type.
# str -> str
def get_command_type(line):
    line = line.split(' ', 1)
    return line[0]

# Returns the command definition.
# str -> str
def get_command_definition(line):
    line = line.split(' ', 1)
    return line[1]

# Returns true if the given line was commented out.
# str -> bool
def is_line_commented(line):
    return len(line) >= 2 and line[0:2] == constants.COMMENT_OUT_STRING

# Given a function and it's perameter returns a function object.
# (str -> anything), str -> (none -> anything)
def function_maker(input_func, perameter):
    return lambda: input_func(perameter)

# Checks that a given type is valid.
# If not, throw an exception.
# str -> none or error
def check_type(type):
    if type not in get_type_map():
        raise ValueError(type + ' is not a valid type')

# Checks that a given line in the config is valid.
# If not, throw an exception.
# str -> none or error
def check_config_line(line):
    if len(line.split(' ', 1)) == 1:
        raise ValueError('Invalid config line: ' + line)

# Returns a map of type names to input functions.
# none -> map of str to (str -> anything)
def get_type_map():
    return {
        'value' : user_enter_value,
        'time' : user_enter_time,
        'did_do' : user_enter_did_do,
        'note' : user_enter_note,
        'key_event' : user_enter_key_event,
        'state_change' : user_enter_state_change
        }

# Runs the program.
def main():

    mockConfig = ['value (0,10) stuff", "time Some stuff", "did_do otherStuff']

    input_functions = config_to_functions(mockConfig)

    for func in input_functions:
        func()

main()