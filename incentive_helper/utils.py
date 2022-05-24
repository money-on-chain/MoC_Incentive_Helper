import json


def options_to_settings(json_content, filename='settings.json'):
    """ Options to file settings.json """

    with open(filename, 'w') as f:
        json.dump(json_content, f, indent=4)
