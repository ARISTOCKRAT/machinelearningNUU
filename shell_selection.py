"""
There we will select shell obj
"""

# TODO: shell_selection:    add more algorithms


def get_shell(instance=None):

    import datetime
    path = instance.path
    file = open(path + '\\output_data\\shell4_border.data', mode='w')
    file.write(str(datetime.datetime.now()))

    file.write("\n\n")
    shell = set()

    debugf = open(path + '\\output_data\\shell_debug.data', mode='w')
    debugf.write(str(datetime.datetime.now()))
    debugf.write('\n\n')

    error_file = open(path + '\\output_data\\shell4_error.data', mode='w')
    error_file.write(str(datetime.datetime.now()))
    error_file.write("\n\n")

    for host_id in instance.ids:
        # DEBUG
        near = instance.get_rel_of(host_id)
        file.write(f":: HOST ID {host_id} data:\n{near}::\n")

        # forming friendly <O(Si)> objects set
        friends = set()
        nearest_opponent_id = None
        for n, row in enumerate(near):
            if row[2] != instance.labels[host_id]:
                nearest_opponent_id = int(row[0])
                break
            else:
                friends.add(int(row[0]))
        friends.add(host_id)

        file.write(f":: f.len = {len(friends)} id,R,class={near}"
                   f"friends: len={len(friends)} {friends}::\n")

        # Seeking nearest obj to nearest_opponent from host_id friends
        shell_obj = [host_id, float('+inf')]
        # print(f"type: {type(nearest_opponent_id)} -- {nearest_opponent_id}; f:{friends}")
        for other_id in friends:
            if instance.rel[nearest_opponent_id][other_id] < shell_obj[1]:
                shell_obj[0] = other_id
                shell_obj[1] = instance.rel[nearest_opponent_id][other_id]
        shell.add(shell_obj[0])
        s = f"f_id, \t\th->f, \t\tf->o, \t\tin border?\n"
        s = f"host_id: {host_id}; opponent:{nearest_opponent_id}; friends:{friends} \n" \
            f"shell_obj: {shell_obj}" \
            f"\nhost_rel:\n{instance.get_rel_of(host_id)}\n" \
            f"\nopp_rel: \n{instance.get_rel_of(nearest_opponent_id)}\n\n"
        debugf.write(s)

    return shell

