import os
from incentive_helper.main import IncentiveHelper


if __name__ == '__main__':

    filter_info = dict()
    filter_info['account'] = '0x199581b423d9707b4b49921ce740c4e4856f0da9'
    filter_info['date_from'] = '2022-04-28 00:00:00'
    filter_info['date_end'] = '2022-05-10 00:00:00'

    config = dict()
    config['config_network'] = 'mocMainnet2'
    config['connection_network'] = 'rskMainnetPublic'
    config['mongo_uri'] = 'mongodb://localhost:27017/'
    config['mongo_db'] = 'doc_mainnet_rewards'
    config['path_report'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'report')

    incentive_helper = IncentiveHelper(config)
    incentive_helper.report_incentive_account(filter_info)


