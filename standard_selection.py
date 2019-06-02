"""
Here would be standart obj selection methods
"""

import datetime
import time


def get_standard(instance):
    if instance.st.logging:
        return method_nuu_with_log(instance)
    else:
        return method_nuu_without_log(instance)


# The method of National University of Uzbekistan
def method_nuu_NeedToComplete(instance):
    # TODO: validate GROUPS
    # TODO: change open file mode into a+

    start_time = time.time()

    # sorting groups by their length. It is IMPORTANT
    # cuz this grands us the only solution
    groups = instance.groups.copy()  # groups
    groups.sort(key=len, reverse=True)  # largest to smallest

    st = instance.st                    # settings
    etalons = instance.ids.copy()       # set of id numbers
    notetalons = set()                  # init values of notetalon objs

    # region LOG_FILES
    standard_file = open(st.path.standard_log, mode='w')
    standard_file.write(str(datetime.datetime.now()))
    standard_file.write("\n\n")
    standard_file.write(f"init_data:: groups:\n")
    for item in groups:
        standard_file.write(f"{str(item)} \n")
    # print(f"init_data:: groups: {groups}\n")

    # handle validator
    if groups is None:
        standard_file.write(f'DD groups not valid. groups{groups} \n')
        return None

    # endregion LOG_FILES

    # WORKING IN EACH GROUP SEPARATELY
    for group in groups:

        # create indent for each element in the group
        indent = list()  # For list of elements ordered by R to nearest_opponent

        # Sorting all elements by R_to_nearest_opponent
        for host_id in group:
            # indent[ <id>, <R>]:
            #         <id>     - id of group element;
            #         <R>      - R to nearest_element;  # for sorting
            indent.append([
                host_id,
                instance.get_nearest_opponent(host_id)[st.rel_of.radius]
            ])
        indent = sorted(indent, key=lambda x: x[1], reverse=False)
        indent = [x[0] for x in indent]  # keep only ids

        standard_file.write(f"\n\nchoose group:: {group}\n")
        standard_file.write(f"Indent elements sorted by R_to_nearest_opponent:: {indent[:]}\n\n")
        # print(f"\n\nchoose group:: {group}\n")
        # print(f"Indent elements sorted by R_to_nearest_opponent:: {indent}\n\n")

        # working in each ELEMENT of GROUP
        for n, candidate_to_del in enumerate(indent):

            # temporary delete from etalons
            etalons.discard(candidate_to_del)
            notetalons.add(candidate_to_del)

            standard_file.write(f"\nS[{candidate_to_del}] label:{int(instance.labels[candidate_to_del])} "
                                f"temporary deleted from etalons. \n")
            # print(f"S[{candidate_to_del}] temporary deleted from etalons. ")

            # CHECK for errors on change etalon_label
            rel_of_candidate = instance.get_rel_of(candidate_to_del)
            # r_to_nearest_opponent_of_candidate = instance.get_nearest_opponent(st.rel_of.radius)

            # looking for nearest obj to candidate
            # minimum: (<id of nearest obj>, <R to nearest obj>, <label of nearest obj>)
            minimum = (-1, float('+inf'), -1)
            for row in rel_of_candidate:
                # if int(row[st.rel_of.idn]) in etalons:
                if (row[st.rel_of.label] == instance.labels[candidate_to_del] and
                        int(row[st.rel_of.idn]) in etalons) or \
                        instance.labels[candidate_to_del] != row[st.rel_of.label]:

                    # Rs === Radius to nearest opponent of min.obj
                    Rs = instance.get_nearest_opponent(int(row[st.rel_of.idn]))[st.rel_of.radius]
                    # Rs_near = instance.get_rel_of(int(row[st.rel_of.idn]))
                    # Rs = 1

                    # print(f"{row[st.rel_of.radius]} / {Rs}")

                    local_metric = row[st.rel_of.radius] / Rs

                    # if row[st.rel_of.radius]:
                    #     local_metric = Rs / row[st.rel_of.radius]
                    # else:
                    #     local_metric = Rs

                    if local_metric < minimum[1]:
                        # DEBUG
                        s = f"\nrow:{row}. S[{int(row[st.rel_of.idn])}] in etalons. \t" \
                            f"local_metric = {row[st.rel_of.radius]} / {Rs} = {local_metric}\n"
                        # print(s)
                        standard_file.write(s)

                        minimum = (row[st.rel_of.idn], local_metric, row[st.rel_of.label])
                else:
                    # print(f"{st.rel_of.idn} not in etalons. ", end='\t')
                    standard_file.write(f"S[{int(row[st.rel_of.idn])}] not in etalons. \t")
            # we've found nearest obj to candidate
            # print(f"minimum: {minimum}")
            standard_file.write(f"\nNearest obj to the candidate is: {minimum}.\n")

            # check for condition 4.
            if instance.labels[candidate_to_del] != minimum[2]:  # if nearest obj CKt
                # return candidate to the etalons
                etalons.add(candidate_to_del)
                notetalons.discard(candidate_to_del)

                standard_file.write(f"S[{candidate_to_del}] returned to the etalons. \n\n")
                # print(f"S[{candidate_to_del}] returned to the etalons. \n")   # DEBUG
            else:  # if nearest obj => Kt, then do nothing
                standard_file.write(f"S[{candidate_to_del}] permanently deleted from etalons. \n\n")
                # print(f"S[{candidate_to_del}] permanently deleted from etalons. \n")  # DEBUG

    standard_file.write("\n\n" + "="*50 + '\n\n')
    standard_file.write(f"standard obj: {etalons}"
                        f"\n\nTIME:: time spend: {time.time() - start_time:.3f}")
    return etalons


def method_nuu_longtime(instance):

    start_time = time.time()

    # sorting groups by their length. It is IMPORTANT
    # cuz this grands us the only solution
    groups = instance.groups.copy()  # groups
    groups.sort(key=len, reverse=True)  # largest to smallest

    st = instance.st                    # settings
    etalons = instance.ids.copy()       # set of id numbers
    notetalons = set()                  # init values of notetalon objs

    # region LOG_FILES
    log = instance.st.logging
    standard_file = None
    if log:
        standard_file = open(st.path.standard_log, mode='w')
        standard_file.write(str(datetime.datetime.now()))
        standard_file.write("\n\n")
        standard_file.write(f"init_data:: groups:\n")
        for item in groups: standard_file.write(f"{str(item)} \n")

    # handle validator
    if groups is None:
        if log:
            standard_file.write(f'DD groups not valid. groups{groups} \n')
        return None

    # endregion LOG_FILES

    # WORKING IN EACH GROUP SEPARATELY
    for group in groups:

        # create indent for each element in the group
        indent = list()  # For list of elements ordered by R to nearest_opponent

        # Sorting all elements by R_to_nearest_opponent
        for host_id in group:
            # indent[ <id>, <R>]:
            #         <id>     - id of group element;
            #         <R>      - R to nearest_element;  # for sorting
            indent.append([
                host_id,
                instance.get_nearest_opponent(host_id)[st.rel_of.radius]
            ])
        indent = sorted(indent, key=lambda x: x[1], reverse=False)
        indent = [x[0] for x in indent]  # keep only ids

        if log:
            standard_file.write(f"\n\nchoose group:: {group}\n")
            standard_file.write(f"Indent elements sorted by R_to_nearest_opponent:: {indent[:]}\n\n")
        # print(f"\n\nchoose group:: {group}\n")
        # print(f"Indent elements sorted by R_to_nearest_opponent:: {indent}\n\n")

        # working in each ELEMENT of GROUP
        for n, candidate_to_del in enumerate(indent):

            # temporary delete from etalons
            etalons.discard(candidate_to_del)
            notetalons.add(candidate_to_del)

            if log:
                standard_file.write(f"\nS[{candidate_to_del}] label:{int(instance.labels[candidate_to_del])} "
                                    f"temporary deleted from etalons. \n")
            # print(f"S[{candidate_to_del}] temporary deleted from etalons. ")

            if is_correct(instance, etalons, notetalons, log_file=standard_file):
                if log: standard_file.write(f"\nS[{candidate_to_del}] permanently DELETED from etalons")
            else:
                etalons.add(candidate_to_del)
                notetalons.discard(candidate_to_del)
                if log: standard_file.write(f"\nS[{candidate_to_del}] RETURNed into etalons")
    if log:
        standard_file.write("\n\n" + "="*50 + '\n\n')
        standard_file.write(f"standard obj: {etalons}"
                            f"\n\nTIME:: time spend: {time.time() - start_time:.3f}")
    return etalons


def method_nuu_with_log(instance):

    start_time = time.time()

    # sorting groups by their length. It is IMPORTANT
    # cuz this grands us the only solution
    groups = instance.groups.copy()  # groups
    # groups.sort(key=len, reverse=True)  # largest to smallest

    st = instance.st                    # settings
    etalons = instance.ids.copy()       # set of id numbers
    notetalons = set()                  # init values of notetalon objs

    # region LOG_FILES
    log = instance.st.logging
    standard_file = None
    if log:
        standard_file = open(st.path.standard_log, mode='w')
        standard_file.write(str(datetime.datetime.now()))
        standard_file.write("\n\n")
        standard_file.write(f"init_data:: groups:\n")
        for item in groups: standard_file.write(f"{str(item)} \n")

    # handle validator
    if groups is None:
        if log: standard_file.write(f'DD groups not valid. groups{groups} \n')
        return None

    # endregion LOG_FILES

    # WORKING IN EACH GROUP SEPARATELY
    for group in groups:

        # create indent for each element in the group
        indent = list()  # For list of elements ordered by R to nearest_opponent

        # Sorting all elements by R_to_nearest_opponent
        for host_id in group:
            # indent[ <id>, <R>]:
            #         <id>     - id of group element;
            #         <R>      - R to nearest_element;  # for sorting
            indent.append([
                host_id,
                instance.get_nearest_opponent(host_id)[st.rel_of.radius]
            ])
        indent = sorted(indent, key=lambda x: x[1], reverse=False)
        indent = [x[0] for x in indent]  # keep only ids

        if log:
            standard_file.write(f"\n\nchoose group:: {group}\n"
                                f"Indent elements sorted by R_to_nearest_opponent:: {indent[:]}\n\n")

        # working in each ELEMENT of GROUP
        for n, candidate_to_del in enumerate(indent):

            # temporary delete from etalons
            etalons.discard(candidate_to_del)
            notetalons.add(candidate_to_del)

            if log:
                standard_file.write(f"\nS[{candidate_to_del}] label:{int(instance.labels[candidate_to_del])} "
                                    f"temporary deleted from etalons. \n")
            # print(f"S[{candidate_to_del}] temporary deleted from etalons. ")
            #######################################################################
            for notetalon_id in notetalons:  # for each notetalon obj
                nearest = (-1, float('inf'))  # looking for nearest opp from etalons
                if log: standard_file.write(f"\nchoose notetalon: {notetalon_id} ::\t ")

                #
                for row in instance.get_rel_of(notetalon_id):
                    if int(row[instance.st.rel_of.idn]) in etalons:
                        Rs = row[instance.st.rel_of.radius] / \
                             instance.get_nearest_opponent(int(row[instance.st.rel_of.idn]))[1]
                        if Rs < nearest[1]:
                            nearest = (row[instance.st.rel_of.idn], Rs)

                        if log: standard_file.write(f":\t{nearest}")
                if nearest[0] == -1:  # if nearest obj has not found, then print error
                    # DEBUG
                    if log:
                        standard_file.write(f"ERROR: standard_selection.is_correct:: NEAREST has not found\n"
                                            f" nearest[eid][ro][nid] = {nearest} ")
                        print(f"ERROR: standard_selection.is_correct:: NEAREST has not found\n"
                              f" nearest[eid][ro][nid] = {nearest} ")
                if instance.labels[int(nearest[0])] != instance.labels[notetalon_id]:
                    etalons.add(candidate_to_del)
                    notetalons.discard(candidate_to_del)
                    if log: standard_file.write(
                        f"\n::correctness violeted:: nearest {nearest} "
                        f"labels[{notetalon_id}] = {instance.labels[notetalon_id]}")
                    break
                #     return False
            # return True
            #######################################################################
            # if is_correct(instance, etalons, notetalons, log_file=standard_file):
            #     ...
            if log: standard_file.write(f"\nS[{candidate_to_del}] permanently DELETED from etalons")
            # else:
            #     etalons.add(candidate_to_del)
            #     notetalons.discard(candidate_to_del)
            #   # if log: standard_file.write(f"\nS[{candidate_to_del}] RETURNed into etalons")
    if log:
        standard_file.write("\n\n" + "="*50 + '\n\n')
        standard_file.write(f"standard obj: {etalons}"
                            f"\n\nTIME:: time spend: {time.time() - start_time:.3f}")
    return etalons


def method_nuu_without_log(instance):
    groups = instance.groups.copy()

    st = instance.st
    etalons = instance.ids.copy()
    notetalons = set()

    for group in groups:
        indent = list()
        for host_id in group:
            indent.append([
                host_id,
                instance.get_nearest_opponent(host_id)[st.rel_of.radius]
                ])
        indent = sorted(indent, key=lambda x: x[1], reverse=False)
        indent = [x[0] for x in indent]

        for n, candidate_to_del in enumerate(indent):
            etalons.discard(candidate_to_del)
            notetalons.add(candidate_to_del)
            for notetalon_id in notetalons:
                nearest = (-1, float('inf'))
                for row in instance.get_rel_of(notetalon_id):
                    if int(row[instance.st.rel_of.idn]) in etalons:
                        Rs = row[instance.st.rel_of.radius] / \
                             instance.get_nearest_opponent(int(row[instance.st.rel_of.idn]))[1]
                        if Rs < nearest[1]:
                            nearest = (row[instance.st.rel_of.idn], Rs)
                if instance.labels[int(nearest[0])] != instance.labels[notetalon_id]:
                    etalons.add(candidate_to_del)
                    notetalons.discard(candidate_to_del)
                    break
    return etalons


def get_standart_old(instance, groups, st):

    # TODO: validate GROUPS
    groups = instance.groups

    # region LOG_FILES
    standart_file = open(st.path.standard_log, mode='w')
    standart_file.write(str(datetime.datetime.now()))
    standart_file.write("\n\n")
    standart_file.write(f"init_data:: groups: {groups}\n")

    # handle validator
    if groups is None:
        s = f'DD groups not valid. groups{groups} \n'
        standart_file.write(s)
        # print(s)
        return None

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


def is_correct(instance, etalons, notetalons, log_file):
    """
    Check for correction of decision

    :param instance:        instance of DataDic
    :param etalons:         set of standard objs
    :param notetalons:      set of not_standard objs. notetalon = E0\etalons
    :param log_file:        log file for save output
    :return:                1 === correct, 0 === error on test
    """

    log = instance.st.logging

    for notetalon_id in notetalons:   # for each notetalon obj
        nearest = (-1, float('inf'))  # looking for nearest opp from etalons
        if log:
            log_file.write(f"\nchoose notetalon: {notetalon_id} ::\t ")

        for etalon_id in etalons:
            Rs = instance.distance(etalon_id, notetalon_id) / instance.get_nearest_opponent(etalon_id)[1]
            if Rs < nearest[1]:  # looking for nearest opp from etalons
                nearest = (etalon_id, Rs)
                if log:
                    log_file.write(f":\t{nearest}")
        if nearest[0] == -1:  # if nearest obj has not found, then print error
            # DEBUG
            if log:
                log_file.write(f"ERROR: standard_selection.is_correct:: NEAREST has not found\n"
                               f" nearest[eid][ro][nid] = {nearest} ")
            print(f"ERROR: standard_selection.is_correct:: NEAREST has not found\n"
                  f" nearest[eid][ro][nid] = {nearest} ")
        if instance.labels[nearest[0]] != instance.labels[notetalon_id]:
            if log:
                log_file.write(f"\n::correctness violeted:: nearest {nearest} "
                               f"labels[{notetalon_id}] = {instance.labels[notetalon_id]}")
            return False
    return True

