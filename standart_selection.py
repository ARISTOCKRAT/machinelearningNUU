"""
Here would be standart obj selection methods
"""

import datetime


def get_standart(instance, groups, st):

    # region LOG_FILES
    standart_file = open(st.path.standart_log, mode='w')
    standart_file.write(str(datetime.datetime.now()))
    standart_file.write("\n\n")
    standart_file.write(f"init_data:: groups: {groups}\n")

    # endregion LOG_FILES

    # sorting groups by their length. It is IMPORTANT
    # cuz this grands us the only solution

    # groups_list = list(groups.values())
    groups_list = groups

    groups_list.sort(key=len, reverse=True)  # largest to smallest
    etalons_list = []

    notetalons = set()

    # group_etalons_list = []
    # WORKING IN EACH GROUP SEPARATELY
    for group in groups_list:
        s = f"\n\n" \
            f"choose group:: {group}\n"
        standart_file.write(s)

        # declare all obj in group as etalons
        group_etalons = group.copy()

        # create indent for each element
        indent = list()  # For list of elements ordered by R to nearest_opponent

        for host_id in group:
            # indent[ <id>, <R> <etalon> ] :
            #         <id>     - id of group element;
            #         <R>      - R to nearest_element;  # for sorting
            #         <etalon> - is this obj etalon?
            indent.append([
                host_id,
                instance.get_nearest_opponent(host_id)[1],
                1
            ])

        # Sorting all elements by R_to_nearest_opponent
        indent = sorted(indent, key=lambda x: x[1], reverse=False)

        # working in each ELEMENT of GROUP
        for n, item in enumerate(indent):

            s = f"Indent elements sorted by R_to_nearest_opponent:: {indent}\n\n"
            standart_file.write(s)

            # temporary delete from group_etalons  # indent[n][2] = 0
            # print(f"del [{item[0]}]", end="\t")
            group_etalons.discard(item[0])
            notetalons.add(item[0])

            # CHECK for errors on change etalon_label
            for notetalon_id in group - group_etalons:
                relation_table = []
                # for other_id in dd['ids'] - \
                #                 (group - group_etalons) - \
                #                 {notetalon_id, }:
                #     # other_id: any, except notetalon objects
                #     relation_table.append([  #
                #         other_id,  # id
                #         dd[notetalon_id]['rel'][other_id],  # R to other_id
                #     ])
                # minimum = min(relation_table, key=lambda x: x[1])
                rel_of_notetalon_id = instance.get_rel_of(notetalon_id)

                kNN_k = 1  # TODO: READ FROM SETTINGS
                opponent_counter = friend_counter = 0
                tmp_etalons = instance.ids - notetalons

                s = f"\nrel_of_notetalon_id{notetalon_id}: \n{rel_of_notetalon_id}"
                standart_file.write(s)

                # counting friend/opponent numbers
                for row in rel_of_notetalon_id:
                    if row[1] in tmp_etalons:  # TODO: row[?] read from st
                        if row[2] == instance.labels[notetalon_id]:
                            friend_counter += 1
                        else:
                            opponent_counter += 1
                    else:
                        continue
                    if friend_counter + opponent_counter > kNN_k:
                        break

                s = f"\nfriend_counter={friend_counter}; opponnt_counter={opponent_counter}"
                standart_file.write(s)
                if friend_counter > opponent_counter:
                    notetalons.discard(notetalon_id)
                    group_etalons.add(notetalon_id)
                    s = f"\n" \
                        f"cuz friends > opps. {notetalon_id} returned to " \
                        f"group_etalons:{group_etalons}\n" \
                        f"notetalons:{notetalons}"
                    standart_file.write(s)
                else:
                    s = f"\n" \
                        f"cuz friends <= opps. {notetalon_id} deleted from" \
                        f"group_etalons:{group_etalons}\n" \
                        f"notetalons:{notetalons}"
                    standart_file.write(s)

        etalons_list.append(group_etalons)
    # DEBUG
    etalons_set = set()
    for etal in etalons_list:
        etalons_set = etalons_set | etal
    # return etalons_list
    return etalons_set


'''

                if dd[notetalon_id]['class'] != dd[minimum[0]]['class']:
                    print(
                        f"ERROR: n{n} NotEtalon{notetalon_id}, "
                        f"minimum{minimum}", end='\t')
                    group_etalons.add(item[0])
                else:
                    print('!', end='')

        group_etalons_list.append(group_etalons)
        print(f"\nGROUP ETALONS: {group_etalons}")

'''
"""
def get_standart(groups):    
    # ordered_list = []
    # WORKING IN EACH GROUP SEPARATELY
    group_etalons_list = []
    for group in groups_list:
    
        group_etalons = group.copy()
    
        ordered_list = list()  # For list of elements ordered by R to nearest_opponent
        for host_id in group:
            #  ordered_list[ <id>, <R> <etalon> ] :
            #                <id>     - id of group element;
            #                <R>      - R to nearest_element;  # for sorting
            #                <etalon> - is this obj etalon?
            ordered_list.append([
                host_id,
                dd[host_id]['nearest_opponent'][1],
                1
            ])
    
        # Sorting all elements by R to nearest_opponent
        ordered_list = sorted(ordered_list, key=lambda x: x[1], reverse=False)
    
        # WORKING ON EACH ELEMENT OF GROUP
        for n, item in enumerate(ordered_list):
    
            # temporary delete from group_etalons  # ordered_list[n][2] = 0
            print(f"del [{item[0]}]", end="\t")
            group_etalons.discard(item[0])
    
            # CHECK for errors on change etalon_label
            for notetalon_id in group - group_etalons:
                relation_table = []
                for other_id in dd['ids'] - \
                                (group - group_etalons) - \
                                {notetalon_id, }:
                    # other_id: any, except notetalon objects
                    relation_table.append([  #
                        other_id,  # id
                        dd[notetalon_id]['rel'][other_id],  # R to other_id
                    ])
                minimum = min(relation_table, key=lambda x: x[1])
    
                if dd[notetalon_id]['class'] != dd[minimum[0]]['class']:
                    print(
                        f"ERROR: n{n} NotEtalon{notetalon_id}, "
                        f"minimum{minimum}", end='\t')
                    group_etalons.add(item[0])
                else:
                    print('!', end='')
    
        group_etalons_list.append(group_etalons)
        print(f"\nGROUP ETALONS: {group_etalons}")

"""

