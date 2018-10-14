import pandas as pd
epsilon = 10**-7


def load_data(file_path="init_data\\data.csv"):


    data_dict = dict()  # returning data
    id_num = 0          # identification number of line
    ids = set()         # set of valid identification numbers

    file = open(path + file, mode='r')
    line = file.readline()
    print(f"В файле с белым вином: {line.strip()} записей, ")  # DEBUG

    line = file.readline()  # EoF white wine
    while line:

        frame = []
        line = line.strip()
        line = line.strip('"\n')
        line = line.split()
        for el in line: frame.append(float(el))

        # all data about one line of df
        data_dict[id_num] = {'id': id_num, 'data': frame}
        if id_num < 100:
            data_dict[id_num]['class'] = 0
        else:
            data_dict[id_num]['class'] = 1

        ids.add(id_num)
        id_num += 1

        line = file.readline()  # EoF white wine

    data_dict['feature_names'] = [
        "feature1",
        "feature2",
    ]

    data_dict['ids'] = ids.copy()

    data_dict['rows'] = id_num - 1

    data_dict['cols'] = len(data_dict[0]['data'])

    data_dict['path'] = path

    return data_dict.copy()


def get_rel(data_dictionary=None):
    """ RELATIVE DICTIONARY CREATING ***************************************
    data_dict[<id_number>]        === dict with all data about object
    data_dict[<id_number>]['rel'] === relative dict, it is next structure
    data_dict[<id_number>]['rel'] === {<id>, <r>}, where 
                                      <id>  = id number of another obj
                                      <r>   = distance to another obj
    ******************************************************************** """

    data_dict = data_dictionary.copy()
    del data_dictionary

    for id_host in data_dict['ids']:  # viewing obj

        rel_dict = dict()
        for id_other in data_dict['ids']:  # for checking distance with another obj

            if id_host == id_other:
                continue
            else:
                r = .0  # distance between objects
                for host_feature, other_feature in \
                        zip(data_dict[id_host]['data'], data_dict[id_other]['data']):
                    r += (other_feature - host_feature) ** 2

                r = r ** (1 / 2)
                rel_dict[id_other] = r

        data_dict[id_host]['rel'] = rel_dict.copy()

    return data_dict.copy()


def get_near(data_dict=None):
    """ GETTING ID AND Radius OF NEAREST OPPONENT *******************************
        data_dict[<id_number>]                     === dict with all data about object
        data_dict[<id_number>]['nearest_opponent'] === list with next structure
        data_dict[<id_number>]['nearest_opponent'] === [0, 1], where 
                                          <id>       = id number of nearest opponent obj
                                          <r>        = distance to nearest opponent obj
        ***************************************************************** """

    for idn in data_dict['ids']:
        data_dict.pop('nearest_opponent', None)

        # getting all opponent ids
        # idn_opponents = {x for x in data_dict['ids']
        #                  if data_dict[x]['class'] != data_dict[idn]['class']}

        # getting id and r of nearest opponent
        mn = (idn, float('+inf'))
        for idn_opp in data_dict['ids']:

            if data_dict[idn]['class'] != data_dict[idn_opp]['class']:
                if mn[1] > data_dict[idn]['rel'][idn_opp]:
                    mn = (idn_opp, data_dict[idn]['rel'][idn_opp])

            # if found r=0, no necessary to continue search
            if mn[1] == .0: break

        # write founding data in to obj
        data_dict[idn]['nearest_opponent'] = mn

    """ CALCULATE K = number of links ***************************************
        data_dict[<id_number>]            === dict with all data about object
        data_dict[<id_number>]['link']    === number of border links 
                                            = (для скольких этот объект является граничным)
    ************************************************************************* """
    for idn in data_dict['ids']:

        near = data_dict[idn]['nearest_opponent']
        if data_dict[near[0]].get('link'):
            data_dict[near[0]]['link'] += 1
        else:
            data_dict[near[0]]['link'] = 1

    return data_dict.copy()  # end of load_data()


def get_shell(data_dict=None):
    """ identify SHELL objects

    :param data_dict:   - data in own dictionary form.
    :return:            - set of shell obj's id_number
    """

    if not data_dict:
        print('Content error')
        return None

    shell = set()  # ids of shell objects
    for host_id in data_dict['ids']:

        near = data_dict[host_id]['nearest_opponent']
        friends = set()
        for friend_id in data_dict['ids']:
            if data_dict[host_id]['class'] == data_dict[friend_id]['class'] and \
                    host_id != friend_id and \
                    data_dict[host_id]['rel'][friend_id] <= near[1]:
                friends.add(friend_id)

        min_from_friends = [host_id, near[1]]
        for friend_id in friends:
            if min_from_friends[1] > data_dict[friend_id]['rel'][near[0]]:
                min_from_friends = [friend_id, data_dict[friend_id]['rel'][near[0]]]

        shell.add(min_from_friends[0])

    return shell  # EoF get_shell


def get_border(data_dict=None):
    """ identify BORDER objects

    :param data_dict:   - data in own dictionary form.
    :return:            - set of border obj's id_number
    """

    try:
        border = set()  # ids of border objects
        for host_id in data_dict['ids']:

            border.add(data_dict[host_id]['nearest_opponent'][0])

        return border.copy()
    except Exception as e:
        print(f'data_dict contents not valid data. {e.args}')
        return set()


def get_noise(data_dict=None, border=None):
    """ identify NOISE objects

        :param data_dict:   - data in own dictionary form.
        :param border:      - IDs of border obj
        :return:            - set of noise obj's id_number
    """

    if not data_dict or not border:
        print('Content error')
        return None

    noise = set()

    for host_id in border:

        K = data_dict[host_id].get('link')              # number of links to the host_if
        R = data_dict[host_id]['nearest_opponent'][1]   # length to nearest opponent
        L = 1                                           # number of friend obj with in R

        for other_id in data_dict['ids']:
            if data_dict[host_id]['class'] == data_dict[other_id]['class'] and \
                            host_id != other_id and \
                            data_dict[host_id]['rel'][other_id] <= R:
                L += 1

        try:
            # if L == 0 or K/L > 1:
            if K/L > 1:
                noise.add(host_id)
        except Exception as e:
            print(f"NOISE ERROR:   id:{host_id:4} K={K:3} L={L:3}\t{e.args}")

    return noise.copy()  # EoF get_noise()

