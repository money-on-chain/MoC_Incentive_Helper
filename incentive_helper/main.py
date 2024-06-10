import datetime
from tabulate import tabulate
import csv
import os

from .base.main import ConnectionHelperMongo
from .base.token import ERC20Token


class IncentiveHelper(object):

    precision = 10 ** 18

    def __init__(self, config):
        self.config = config

    def incentive_account(self, filter_info):

        connection_helper = ConnectionHelperMongo(self.config)

        moc_token = ERC20Token(connection_helper.connection_manager,
                               contract_address=self.config['addresses']['MoCToken'])

        d_from = datetime.datetime.strptime(filter_info["date_from"], '%Y-%m-%d %H:%M:%S')
        d_end = datetime.datetime.strptime(filter_info["date_end"], '%Y-%m-%d %H:%M:%S')

        collection_mocin_rewards = connection_helper.mongo_collection('mocin_rewards')
        collection_mocin_rewards_extscaninfo = connection_helper.mongo_collection('mocin_rewards_extscaninfo')
        collection_mocin_agent_tx = connection_helper.mongo_collection('mocin_agent_tx')

        mocin_rewards = collection_mocin_rewards.find(
            {
                "account_address": filter_info["account"],
                "date": {"$gte": d_from, "$lt": d_end}
            },
            sort=[("date", 1)]
        )

        trace_accounts = list()
        trace_accounts.append(filter_info["account"])

        rewards_list = list()
        for reward in mocin_rewards:
            block_n = reward["reason"]["end_block"]
            moc_rewarded = reward["moc_by_origin"].to_decimal() / self.precision
            bpro_holding = reward["reason"]["bpro_balance"].to_decimal() / self.precision

            ext_info = collection_mocin_rewards_extscaninfo.find_one({"end_block": block_n}, sort=[("end_block", -1)])
            if ext_info:
                total_bpro = ext_info["total_bpro"].to_decimal() / self.precision
            else:
                total_bpro = 0

            info_reward = dict()
            info_reward["action"] = "assigned"
            info_reward["block_n"] = block_n
            info_reward["moc_rewarded"] = moc_rewarded
            info_reward["bpro_holding"] = bpro_holding
            info_reward["total_bpro"] = total_bpro
            info_reward["assigned_date"] = reward["date"]

            if reward["account_address"].lower() != reward["destination_address"].lower():
                info_reward["destination_address"] = reward["destination_address"].lower()
                info_reward["moc_balance"] = moc_token.balance_of(reward["destination_address"], block_identifier=block_n)
                if info_reward["destination_address"] not in trace_accounts:
                    trace_accounts.append(info_reward["destination_address"])
            else:
                info_reward["destination_address"] = ''
                info_reward["moc_balance"] = moc_token.balance_of(reward["account_address"], block_identifier=block_n)

            rewards_list.append(info_reward)

        for trace_account in trace_accounts:
            mocin_agent_tx = collection_mocin_agent_tx.find(
                {
                    "address": trace_account,
                    "state": "complete",
                    "result": "ok",
                    "createdAt": {"$gte": d_from, "$lt": d_end}
                },
                sort=[("sentBlocknr", 1)]
            )

            for agent_tx in mocin_agent_tx:
                info_reward = dict()
                info_reward["action"] = "sent"
                info_reward["block_n"] = agent_tx["sentBlocknr"]
                info_reward["moc_rewarded"] = ""
                info_reward["bpro_holding"] = ""
                info_reward["total_bpro"] = ""
                info_reward["sent_hash"] = agent_tx["sentHash"]
                info_reward["sent_mocs"] = agent_tx["mocs"].to_decimal() / self.precision
                info_reward["sent_date"] = agent_tx["stateTS"]
                info_reward["moc_balance"] = moc_token.balance_of(trace_account,
                                                                  block_identifier=info_reward["block_n"])
                info_reward["destination_address"] = trace_account

                rewards_list.append(info_reward)

        return rewards_list

    @staticmethod
    def report_incentive_account_to_screen(sorted_rewards_list):

        display_table = []
        titles = ['Nº Block',
                  'Action',
                  'MoC Rewarded',
                  'MoC Accumulated',
                  'BPro Holding',
                  'Total BPro System',
                  'Assign Date',
                  'Destination Addr',
                  'User MoC Balance',
                  'Sent Amount',
                  'Sent Date']

        moc_accumulated = 0
        for reward_i in sorted_rewards_list:

            if reward_i["action"] == "assigned":
                moc_rewarded = '%.2f' % reward_i["moc_rewarded"]
                moc_accumulated += reward_i["moc_rewarded"]
                bpro_holding = '%.6f' % reward_i["bpro_holding"]
                total_bpro = '%.6f' % reward_i["total_bpro"]
                assigned_date = reward_i["assigned_date"].strftime('%Y-%m-%d %H:%M')
                sent_amount = ""
                sent_date = ""
                user_moc_balance = '%.6f' % reward_i["moc_balance"]
                sent_hash = ""
            elif reward_i["action"] == "sent":
                moc_accumulated = 0
                moc_rewarded = ""
                bpro_holding = ""
                total_bpro = ""
                assigned_date = ""
                sent_amount = '%.6f' % reward_i["sent_mocs"]
                sent_date = reward_i["sent_date"].strftime('%Y-%m-%d %H:%M:%S')
                user_moc_balance = '%.6f' % reward_i["moc_balance"]
                sent_hash = reward_i["sent_hash"]
            else:
                continue

            display_table.append(
                [
                    reward_i["block_n"],
                    reward_i["action"],
                    moc_rewarded,
                    '%.6f' % moc_accumulated,
                    bpro_holding,
                    total_bpro,
                    assigned_date,
                    reward_i["destination_address"],
                    user_moc_balance,
                    sent_amount,
                    sent_date
                ]
            )

        print(tabulate(display_table, headers=titles, tablefmt="pipe"))

    def report_incentive_account_to_csv(self, sorted_rewards_list, filter_info):

        columns = ['Nº Block',
                   'Action',
                   'MoC Rewarded',
                   'MoC Accumulated',
                   'BPro Holding',
                   'Total BPro System',
                   'Assign Date',
                   'Destination Addr',
                   'User MoC Balance',
                   'Sent Amount',
                   'Sent Date',
                   'Sent Hash']

        d_from = datetime.datetime.strptime(filter_info["date_from"], '%Y-%m-%d %H:%M:%S')
        d_end = datetime.datetime.strptime(filter_info["date_end"], '%Y-%m-%d %H:%M:%S')

        file_name = 'report_account_{0}_{1}_{2}.csv'.format(
            filter_info["account"],
            d_from.strftime("%Y-%m-%d"),
            d_end.strftime("%Y-%m-%d"))

        destination_file = os.path.join(self.config['path_report'], file_name)

        with open(destination_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(columns)

            count = 0
            moc_accumulated = 0
            for reward_i in sorted_rewards_list:
                count += 1

                if reward_i["action"] == "assigned":
                    moc_rewarded = '%.6f' % reward_i["moc_rewarded"]
                    moc_accumulated += reward_i["moc_rewarded"]
                    bpro_holding = '%.6f' % reward_i["bpro_holding"]
                    total_bpro = '%.6f' % reward_i["total_bpro"]
                    assigned_date = reward_i["assigned_date"].strftime('%Y-%m-%d %H:%M')
                    sent_amount = ""
                    sent_date = ""
                    user_moc_balance = '%.6f' % reward_i["moc_balance"]
                    sent_hash = ""
                elif reward_i["action"] == "sent":
                    moc_accumulated = 0
                    moc_rewarded = ""
                    bpro_holding = ""
                    total_bpro = ""
                    assigned_date = ""
                    sent_amount = '%.6f' % reward_i["sent_mocs"]
                    sent_date = reward_i["sent_date"].strftime('%Y-%m-%d %H:%M:%S')
                    user_moc_balance = '%.6f' % reward_i["moc_balance"]
                    sent_hash = reward_i["sent_hash"]
                else:
                    continue

                row = [
                        reward_i["block_n"],
                        reward_i["action"],
                        moc_rewarded,
                        moc_accumulated,
                        bpro_holding,
                        total_bpro,
                        assigned_date,
                        reward_i["destination_address"],
                        user_moc_balance,
                        sent_amount,
                        sent_date,
                        sent_hash
                    ]
                writer.writerow(row)

    def report_incentive_account(self, filter_info):

        rewards_list = self.incentive_account(filter_info)
        sorted_rewards_list = sorted(rewards_list, key=lambda k: k['block_n'])
        self.report_incentive_account_to_screen(sorted_rewards_list)
        self.report_incentive_account_to_csv(sorted_rewards_list, filter_info)

    def incentive_accumulated(self, filter_info):

        connection_helper = ConnectionHelperMongo(self.config)

        d_from = datetime.datetime.strptime(filter_info["date_from"], '%Y-%m-%d %H:%M:%S')
        d_end = datetime.datetime.strptime(filter_info["date_end"], '%Y-%m-%d %H:%M:%S')

        collection_mocin_rewards = connection_helper.mongo_collection('mocin_rewards')
        collection_mocin_agent_tx = connection_helper.mongo_collection('mocin_agent_tx')

        mocin_rewards = collection_mocin_rewards.find(
            {
                "date": {"$gte": d_from, "$lt": d_end}
            },
            sort=[("date", 1)]
        )

        accumulated_rewards = dict()
        for reward in mocin_rewards:
            moc_rewarded = reward["moc_by_origin"].to_decimal() / self.precision
            account_address = reward['account_address']

            if account_address in accumulated_rewards:
                accumulated_rewards[account_address] = accumulated_rewards[account_address] + moc_rewarded
            else:
                accumulated_rewards[account_address] = moc_rewarded

        mocin_agent_tx = collection_mocin_agent_tx.find(
            {
                "state": "complete",
                "result": "ok",
                "createdAt": {"$gte": d_from, "$lt": d_end}
            },
            sort=[("sentBlocknr", 1)]
        )

        accumulated_sent = dict()
        for agent_tx in mocin_agent_tx:
            account_address = agent_tx['address']
            sent_mocs = agent_tx["mocs"].to_decimal() / self.precision

            if account_address in accumulated_sent:
                accumulated_sent[account_address] = accumulated_sent[account_address] + sent_mocs
            else:
                accumulated_sent[account_address] = sent_mocs

        report_accumulated = list()
        for account in accumulated_rewards:
            info = dict()
            info['account'] = account
            info['rewarded'] = accumulated_rewards[account]
            if account in accumulated_sent:
                info['sent'] = accumulated_sent[account]
                info['pending'] = info['rewarded'] - info['sent']
            else:
                info['sent'] = 0
                info['pending'] = info['rewarded']

            report_accumulated.append(info)

        return report_accumulated

    def report_incentive_accumulated(self, filter_info):

        report_accumulated = self.incentive_accumulated(filter_info)
        self.report_incentive_accumulated_to_screen(report_accumulated)
        self.report_incentive_accumulated_to_csv(report_accumulated, filter_info)

    @staticmethod
    def report_incentive_accumulated_to_screen(report_accumulated):

        display_table = []
        titles = ['#',
                  'Account',
                  'Total Rewarded',
                  'Total Sent',
                  'Total Pending']

        count = 0
        total_rewarded = 0
        total_sent = 0
        total_pending = 0
        for reward_i in report_accumulated:
            count += 1

            total_rewarded += reward_i["rewarded"]
            total_sent += reward_i["sent"]
            total_pending += reward_i["pending"]

            display_table.append(
                [
                    count,
                    reward_i["account"],
                    reward_i["rewarded"],
                    reward_i["sent"],
                    reward_i["pending"]
                ]
            )

        print(tabulate(display_table, headers=titles, tablefmt="pipe"))

        print("Total Rewarded:", total_rewarded)
        print("Total Sent:", total_sent)
        print("Total Pending:", total_pending)

    def report_incentive_accumulated_to_csv(self, report_accumulated, filter_info):

        columns = ['#',
                   'Account',
                   'Total Rewarded',
                   'Total Sent',
                   'Total Pending']

        d_from = datetime.datetime.strptime(filter_info["date_from"], '%Y-%m-%d %H:%M:%S')
        d_end = datetime.datetime.strptime(filter_info["date_end"], '%Y-%m-%d %H:%M:%S')

        file_name = 'report_accumulated_{0}_{1}.csv'.format(
            d_from.strftime("%Y-%m-%d"),
            d_end.strftime("%Y-%m-%d"))

        destination_file = os.path.join(self.config['path_report'], file_name)

        with open(destination_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(columns)

            count = 0
            for reward_i in report_accumulated:
                count += 1
                row = [
                    count,
                    reward_i["account"],
                    reward_i["rewarded"],
                    reward_i["sent"],
                    reward_i["pending"]
                    ]
                writer.writerow(row)
