import os
from incentive_helper.main import IncentiveHelper


if __name__ == '__main__':

    filter_info = dict()
    filter_info['date_from'] = '2020-10-08 00:00:00'#'2021-05-27 00:00:00'
    filter_info['date_end'] = '2022-12-22 23:59:59' #'2022-07-18 23:59:59'

    config = dict()
    config['config_network'] = 'mocMainnet2'
    config['connection_network'] = 'rskMainnetPublic'
    config['mongo_uri'] = 'mongodb://localhost:27017/'
    config['mongo_db'] = 'doc_mainnet_rewards'
    config['path_report'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'report')

    incentive_helper = IncentiveHelper(config)
    incentive_helper.report_incentive_accumulated(filter_info)


