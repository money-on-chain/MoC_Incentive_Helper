import os
from incentive_helper.main import IncentiveHelper


if __name__ == '__main__':

    filter_info = dict()
    filter_info['account'] = '0x704c900140726f918dd26a6dc009f18b3283afd9'  # 0x2E1F1d826B3C3D4A93468721745998b76cF4bc03
    filter_info['date_from'] = '2020-10-08 00:00:00'
    filter_info['date_end'] = '2022-06-16 23:59:59'

    config = dict()
    config['config_network'] = 'mocMainnet2'
    config['connection_network'] = 'rskMainnetPublic'
    config['mongo_uri'] = 'mongodb://localhost:27017/'
    config['mongo_db'] = 'doc_mainnet_rewards'
    config['path_report'] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'report')

    incentive_helper = IncentiveHelper(config)
    incentive_helper.report_incentive_account(filter_info)


