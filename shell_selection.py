"""
There we will select shell obj
"""
import time
# TODO: shell_selection:    add more algorithms


def get_shell(instance, st):
    import datetime
    st = instance.st
    start_time = time.time()
    # region LOG_FILES
    # path = instance.path  # moved to st

    # border_file = open(st.path.border_after_log, mode='w')
    # border_file.write(str(datetime.datetime.now()))
    # border_file.write("\n\n")

    shell_file = open(st.path.shell_log, mode='w')
    # shell_file = open(st.full_path['shell_log'], mode='w')
    shell_file.write(str(datetime.datetime.now()))
    shell_file.write('\n\n')

    error_file = open(st.path.error_log, mode='w')
    # error_file = open(st.full_path['error_log'], mode='w')
    error_file.write(str(datetime.datetime.now()))
    error_file.write("\n\n")
    # endregion LOG_FILES end

    shell = set()

    for host_id in instance.ids:
        # DEBUG
        near = instance.get_rel_of(host_id)
        # border_file.write(f"\n:: HOST ID {host_id} near:\nid, R, label\n{near}\n")

        # Пока я не понял зачем определять О(Si), т.к.
        # Ближайщим к оппоненту может быть объект не входящий в O(Si) НО! его игнорируем
        # что приводит (ИМХО) к противоречию. TODO: check it!

        # forming friendly <O(Si)> objects set
        friends = set()
        nearest_opponent_id = None
        for n, row in enumerate(near):
            if row[st.rel_of.label] == instance.labels[host_id]:
                friends.add(int(row[st.rel_of.idn]))
            else:
                nearest_opponent_id = int(row[st.rel_of.idn])
                break
        friends.add(host_id)

        # Seeking nearest obj to nearest_opponent from host_id's friendzone
        shell_obj = [host_id, instance.distance(host_id, nearest_opponent_id)]
        # shell_obj = [-1, float('+inf')]
        # print(f"type: {type(nearest_opponent_id)} -- {nearest_opponent_id}; f:{friends}")
        for other_id in friends:
            # if instance.rel[nearest_opponent_id][other_id] < shell_obj[1]:
            if instance.distance(nearest_opponent_id, other_id) < shell_obj[1]:
                shell_obj[0] = other_id
                # shell_obj[1] = instance.rel[nearest_opponent_id][other_id]
                shell_obj[1] = instance.distance(nearest_opponent_id, other_id)
        shell.add(shell_obj[0])

        shell_file.write(
            f"\nhost_id:{host_id}; opponent:{nearest_opponent_id}; "
            f"shell_id: {shell_obj[0]}; friends:{friends} \n"
            # f"h->o: {instance.rel[host_id][nearest_opponent_id]}; "
            f"h->o: {instance.distance(host_id, nearest_opponent_id)}; "
            # f"o->f: {instance.rel[nearest_opponent_id][shell_obj[0]]}; "
            f"o->f: {instance.distance(nearest_opponent_id, shell_obj[0])}; "
            # f"h->f: {instance.rel[host_id][shell_obj[0]]}\n"
            f"h->f: {instance.distance(host_id, shell_obj[0])}\n"
            f"\nhost_rel:\n{instance.get_rel_of(host_id)[:]}\n"
            f"\nopp_rel: \n{instance.get_rel_of(nearest_opponent_id)[:]}\n"
            f"shell:{shell}\n\n"
        )

    shell_file.write("\n\n" + "=" * 50 + '\n\n')
    shell_file.write(f"shell obj: len:{len(shell)}\n {shell}")
    shell_file.write(f"\n\nTIME:: time spend: {time.time() - start_time:.3f}")
    return shell

