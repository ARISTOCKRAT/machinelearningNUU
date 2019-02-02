"""
Here we would group our obj
"""

import numpy as np
import datetime
import time

# TODO: grouping:   add more grouping algorithms
# TODO: grouping:   rework __doc__


def grouping(instance):
    pass


def get_groups(instance, st):

    start_time = time.time()

    # region LOG_FILES
    log = instance.st.logging
    if log:
        binary_file = open(st.path.binary_log, mode='w')
        binary_file.write(str(datetime.datetime.now()))
        binary_file.write("\n\n")
    # endregion LOG_FILES

    binary_dict = {shell_id: {shell_id} for shell_id in instance.shell}

    # binary_dict = dict()
    # for shell_id in instance.shell:
    #     binary_dict[shell_id] = set()
    #     binary_dict[shell_id].add(shell_id)

    for host_id in instance.ids:

        near = instance.get_rel_of(host_id)

        for row in near:
            if instance.labels[host_id] != int(row[st.rel_of.label]):
                break
            else:
                if int(row[st.rel_of.idn]) in instance.shell:
                    binary_dict[int(row[st.rel_of.idn])].add(host_id)

    if log:
        binary_file.write(f"binary dict:\n")
        for item in binary_dict.items(): binary_file.write(f"{item}\n")

    ####
    dirty = True
    while dirty:
        dirty = False
        keys = list(binary_dict.keys()).copy()
        for host_key in keys:
            # print(f"host_key: {host_key}", end=" ")
            for other_key in keys:
                # print(f"other_key: {other_key}; ", end=" ")
                if host_key == other_key:
                    # print('continue1', end='\n')
                    continue
                if binary_dict[host_key] & binary_dict[other_key]:
                    binary_dict[host_key] = binary_dict[host_key] | binary_dict[other_key]
                    # print(f"g[host_key]: {binary_dict[host_key]}")
                    # print(f'del ({host_key}+{other_key}) group[{other_key}]', end='\t')

                    del binary_dict[other_key]
                    dirty = True
                    break
            if dirty:
                # print('break2')
                break
        if dirty: continue

    ####
    groups = list()
    for g in binary_dict.values():
        groups.append(g)

    # sorting groups by their length. It is IMPORTANT
    # cuz this grands us the only solution

    # groups_list = list(groups.values())
    # groups_list = groups

    groups.sort(key=len, reverse=True)  # largest to smallest

    if log:
        binary_file.write("\n" + "="*50 + f'\n groups: len:{len(groups)}\n')
        for item in groups: binary_file.write(f".len{len(item)} {item}\n")
        binary_file.write(f"\n\nTIME:: time spend: {time.time() - start_time:.3f}")
    return groups.copy()


def get_groups2(instance, st):

    start_time = time.time()

    # region LOG_FILES
    binary_file = open(st.path.binary_log[:-4] + '2.log', mode='w')
    binary_file.write(str(datetime.datetime.now()))
    binary_file.write("\n\n")
    # endregion LOG_FILES

    binary_list = []
    for x, shell_id in enumerate(range(len(instance.shell))):
        row = []
        for y, idn in enumerate(range(len(instance.ids))):
            near = instance.get_rel_of(idn)
            # row =
    #######################################################################
    #######################################################################
    binary_dict = {shell_id: {shell_id} for shell_id in instance.shell}

    # binary_dict = dict()
    # for shell_id in instance.shell:
    #     binary_dict[shell_id] = set()
    #     binary_dict[shell_id].add(shell_id)

    for host_id in instance.ids:

        near = instance.get_rel_of(host_id)

        for row in near:
            if instance.labels[host_id] != int(row[st.rel_of.label]):
                break
            else:
                if int(row[st.rel_of.idn]) in instance.shell:
                    binary_dict[int(row[st.rel_of.idn])].add(host_id)

    binary_file.write(f"binary dict:\n")
    for item in binary_dict.items(): binary_file.write(f"{item}\n")

    ####
    dirty = True
    while dirty:
        dirty = False
        keys = list(binary_dict.keys()).copy()
        for host_key in keys:
            # print(f"host_key: {host_key}", end=" ")
            for other_key in keys:
                # print(f"other_key: {other_key}; ", end=" ")
                if host_key == other_key:
                    # print('continue1', end='\n')
                    continue
                if binary_dict[host_key] & binary_dict[other_key]:
                    binary_dict[host_key] = binary_dict[host_key] | binary_dict[other_key]
                    # print(f"g[host_key]: {binary_dict[host_key]}")
                    # print(f'del ({host_key}+{other_key}) group[{other_key}]', end='\t')

                    del binary_dict[other_key]
                    dirty = True
                    break
            if dirty:
                # print('break2')
                break
        if dirty: continue

    ####
    groups = list()
    for g in binary_dict.values():
        groups.append(g)

    # sorting groups by their length. It is IMPORTANT
    # cuz this grands us the only solution

    # groups_list = list(groups.values())
    # groups_list = groups

    groups.sort(key=len, reverse=True)  # largest to smallest

    binary_file.write("\n" + "="*50 + f'\n groups: len:{len(groups)}\n')
    for item in groups: binary_file.write(f".len{len(item)} {item}\n")
    binary_file.write(f"\n\nTIME:: time spend: {time.time() - start_time:.3f}")
    return groups.copy()


if __name__ == '__main__':
    pass
