import os

def rngToTxt(rng_path):
    with open(rng_path) as f:
        l_strip = [s.strip() for s in f.readlines()]
        hand = l_strip[0::2]  # 'AA'
        probability = l_strip[1::2]  # '0.0;-324999.9999999724'

        # 'XX /n 1.0;0.0' > XX:1.0
        range_list = ['{0}:{1}'.format(i, j.split(";")[0]) for i, j in zip(hand, probability)]

        return ','.join(range_list)


def rngNameChanger(rng_filename):
    """
    :param rng_filename: ex) 0.0
    :return: LJ_fold-HJ_fold
    """
    action_separated = rng_filename.split('.')
    player_round = ['LJ', 'HJ', 'CO', 'BTN', 'SB', 'BB']
    now_player_order = 0
    actions_renamed = []

    for j in action_separated:
        action = int(j)
        player_order_surplus = now_player_order % len(player_round)
        now_player = player_round[player_order_surplus]

        if action == 0:  # fold
            now_action = now_player + '_fold'
            actions_renamed.append(now_action)

            player_round.pop(player_order_surplus)  # delete player from player_round

        elif action == 1:  # call
            now_action = now_player + '_call'
            actions_renamed.append(now_action)

            now_player_order += 1

        elif action == 3:  # ALL in
            now_action = '{}_Allin'.format(now_player)
            actions_renamed.append(now_action)

            now_player_order += 1

        elif action > 40000:  # bet(%)
            betSize = str(action - 40000) + '%'  # ex) 40076 - 40000 > 76%
            now_action = now_player + '_' + betSize
            actions_renamed.append(now_action)

            now_player_order += 1

        else:  # bet(sb)
            betSize = str(action) + 'sb'
            now_action = now_player + '_' + betSize
            actions_renamed.append(now_action)

            now_player_order += 1

    return '-'.join(actions_renamed)


# test
sample_rng_path = 'sampleRngFile' # sample/0.0.0.40065.rng
basename_without_ext = os.path.splitext(os.path.basename(sample_rng_path))[0]
print(rngToTxt(sample_rng_path))
print(rngNameChanger(basename_without_ext))
