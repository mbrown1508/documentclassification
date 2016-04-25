__author__ = 'Matthew'


def yes_no_question(question, default=None):
    question_answered = False
    result = False

    if default == True:
        default_string = 'Y/n'
    elif default == False:
        default_string = 'y/N'
    else:
        default_string = 'y/n'

    while not question_answered:
        answer = input('%s %s: ' % (question, default_string))

        if answer.lower() == 'y':
            question_answered = True
            result = True
        elif answer.lower() == 'n':
            question_answered = True
            result = False
        elif answer == '' and default is not None:
            question_answered = True
            result = default
        else:
            print('Please enter a valid option!')

    return result


def get_selection(question, options):
    print(question)

    user_selection = -1
    option_selected = 'No Option'

    selection = False

    while not selection:
        # Loop over all available applications
        for option_index in range(len(options)):
            print('%s. %s' % (option_index + 1, options[option_index]))

        try:
            user_selection = int(input('Please select a option: '))

            if user_selection > 0 and user_selection <= len(options):
                option_selected = options[user_selection - 1]
                selection = True
            else:
                raise ()
        except:
            print('\nPlease select a valid option\n')

    return [user_selection, option_selected]


def get_number(question, default, min, max, float_return=False, percentage=False):
    number_found = False
    return_value = -1

    while not number_found:
        if percentage:
            addin = '%'
        else:
            addin = ''

        return_value = input('%s (%s%s): ' % (question, default, addin))

        if return_value == '':
            return_value = default

        try:
            if not float_return:
                return_value = int(return_value)
            else:
                return_value = float(return_value)

            if return_value >= min and return_value <= max:
                number_found = True
            else:
                raise ()
        except:
            print('Enter a valid number! (%s-%s)' % (min, max))

    return return_value
