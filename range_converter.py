import os

import glob
import pathlib


class RangeConverter_6max:
    def __init__(self, path):
        """
        :param path: rng file path ex) test/test/0.0.0.0.0.rng
        """
        self.path = path

    def pioFileMaker(self):
        """

        :return:range string which PioSolver or GTO+ can read as range
        """
        with open(self.path) as f:
            l_strip = [s.strip() for s in f.readlines()]
            even = l_strip[0::2]
            odd = l_strip[1::2]

            # 'XX /n 1.0;0.0' > XX:1.0
            range_list = ['{0}:{1}'.format(i, j.split(";")[0]) for i, j in zip(even, odd)]

            return ','.join(range_list)

    @property
    def makeActionLine(self):
        """
        :return: action line string
        ex) LJ_open-HJ_3bet-CO_fold-BTN_fold-SB_fold-BB_fold-LJ_4bet-HJ_5betAI
        """
        action_line = os.path.splitext(os.path.basename(self.path))[0]
        action_separated = action_line.split('.')

        player_round = ['LJ', 'HJ', 'CO', 'BTN', 'SB', 'BB']
        now_player_order = 0
        bet_round = ['open', '3bet', '4bet', '5bet']
        now_bet_order = 0
        actions_renamed = []

        for j in action_separated:
            action = int(j)
            if action == 0:  # fold
                player_order_surplus = now_player_order % len(player_round)
                now_action = player_round[player_order_surplus] + '_fold'
                actions_renamed.append(now_action)

                player_round.pop(player_order_surplus)  # delete player from player_round

            elif action == 1:  # call
                player_order_surplus = now_player_order % len(player_round)
                now_action = player_round[player_order_surplus] + '_call'
                actions_renamed.append(now_action)

                now_player_order += 1

            elif action == 3:  # ALL in
                player_order_surplus = now_player_order % len(player_round)
                now_action = '{0}_{1}AI'.format(player_round[player_order_surplus], bet_round[now_bet_order])
                actions_renamed.append(now_action)

                now_player_order += 1

            else:  # bet
                player_order_surplus = now_player_order % len(player_round)
                now_action = player_round[player_order_surplus] + '_' + bet_round[now_bet_order]
                actions_renamed.append(now_action)

                now_bet_order += 1

                now_player_order += 1

        return '-'.join(actions_renamed)


sample_dir = 'Range/sample'
p_temp = [pathlib.Path(i) for i in glob.glob('{}/**'.format(sample_dir), recursive=True)]
f_list = [p for p in p_temp if p.is_file()]
for file in f_list:
    converter = RangeConverter_6max(file)
    print(converter.makeActionLine)
