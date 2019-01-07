
import datetime

# TODO: border_selection: more algorithms for border selection


def get_border(instance):
    """ identify BORDER objects

    :instance:          - instance of DD
    :return:            - set of border obj's id_number
    """

    # region LOG_FILES
    while True:
        try:
            border_file = open(instance.st.path.border_log[:-4] + str(instance.st.counter.border) + '.log',
                               mode='w')
            instance.st.counter.border += 1
            break
        except Exception:
            instance.st.counter.border += 1
            continue

    # border_file = open(st.path.border_before_log, mode='w')
    border_file.write(str(datetime.datetime.now()))
    border_file.write("\n\n")
    # endregion LOG_FILES

    link = dict()

    for host_id in instance.ids:
        link[host_id] = 0

    border = set()  # ids of border objects

    for host_id in instance.ids:  # for each obj
        near = instance.get_rel_of(host_id)  # get relative table of obj

        border_file.write(f"\n S[{host_id}];\t near:\n{near}\n")

        for row in near:          # looking for opponent on row host_id
            # if row[st.row.idn] in instanse.ids:
            if instance.labels[host_id] != int(row[instance.st.rel_of.label]):  # opponent found
                border.add(int(row[instance.st.rel_of.idn]))  # add opponent_id into border_dict
                link[int(row[instance.st.rel_of.idn])] += 1
                border_file.write(f"S[{int(row[instance.st.rel_of.idn])}] now border obj\n")
                break  # stop looking for opponent
        else:  # if no opponent found
            import error_handler
            s = f"ERROR:: no border obj found :: border_selection ::\n" \
                f"\thost_id:{host_id}; row[{host_id}]:{near}\n"
            error_handler.write(s, instance.st)
            border_file.write(s)
        border_file.write(f"border: {border}\n")

    border_file.write("\n" + '='*50 + '\n')
    border_file.write(f"border: len:{len(border)}\n{border}")
    return border.copy(), link.copy()

