import sys


def get_user_input(input_type: dict) -> dict:
    """
    Gathers user input from the command line.

    Returns:
        str: The user input as a string.
    """
    if len(sys.argv) > 1:
        # If command line arguments are provided, use the first one as input
        user_input = sys.argv[1]
    else:
        # If no command line arguments are provided, prompt the user for input
        for field in input_type:
            if type(input_type[field]) == list:
                input_type[field] = [i.strip() for i in str(
                    input("What are your desired {}?: ".format(
                        field +
                        ' (comma separated)'))).lower().split(',')]
            elif type(input_type[field]) == str:
                input_type[field] = input(
                    "What is your desired {}?: ".format(field)).lower()

    # TODO: currently hard coding location to london
    input_type['location'] = 'london'

    return input_type