import os
import json

from incentive_helper.main import IncentiveHelper


def options_from_config(filename=None):
    """ Options from file config.json """

    if not filename:
        filename = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')

    with open(filename) as f:
        options = json.load(f)

    return options


if __name__ == '__main__':

    config = options_from_config()

    # override config default
    if 'APP_CONFIG' in os.environ:
        config = json.loads(os.environ['APP_CONFIG'])

    # override mongo uri from env
    if 'APP_MONGO_URI' in os.environ:
        config['mongo']['uri'] = os.environ['APP_MONGO_URI']

    # override mongo db from env
    if 'APP_MONGO_DB' in os.environ:
        config['mongo']['db'] = os.environ['APP_MONGO_DB']

    # override connection uri from env
    if 'APP_CONNECTION_URI' in os.environ:
        config['uri'] = os.environ['APP_CONNECTION_URI']

    filter_info = dict()
    filter_info['account'] = '0x704c900140726f918dd26a6dc009f18b3283afd9'  # 0x2E1F1d826B3C3D4A93468721745998b76cF4bc03
    filter_info['date_from'] = '2024-04-01 00:00:00'  # 2022-05-21 00:00:00 '2021-05-27 00:00:00'
    filter_info['date_end'] = '2024-05-31 23:59:59'  # 2022-12-22 23:59:59 '2022-07-18 23:59:59'

    config['path_report'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'report')

    report = IncentiveHelper(config)
    report.report_incentive_accumulated(filter_info)
