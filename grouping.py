"""
Here we would group our obj
"""

import numpy as np
# import settings as st

# TODO: grouping:   add more grouping algorithms
# TODO: grouping:   rework __doc__


def grouping(instance):
    pass


def get_groups(instance, settings):

    st = settings

    binary_dict = dict()
    for shell_id in instance.shell:
        binary_dict[shell_id] = set()
        binary_dict[shell_id].add(shell_id)

    for host_id in instance.ids:

        near = instance.get_rel_of(host_id)

        for row in near:
            if instance.labels[host_id] != int(row[st.rel_of.label]):
                break
            else:
                if int(row[st.rel_of.idn]) in instance.shell:
                    binary_dict[int(row[st.rel_of.idn])].add(host_id)

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
        if dirty:
            # print('continue2')
            continue
    ####
    groups = list()
    for g in binary_dict.values():
        groups.append(g)

    return groups.copy()


if __name__ == '__main__':
    pass
