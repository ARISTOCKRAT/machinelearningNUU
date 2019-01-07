
import datetime

# TODO: border_selection: more algorithms for border selection


def get_border(instanse):
    """ identify BORDER objects

    :instance:          - instance of DD
    :return:            - set of border obj's id_number
    """

    st = instanse.st

    # region LOG_FILES
    c = 1
    while True:
        try:
            border_file = open(st.path.border_log[:-4] + str(c) + '.log',
                               mode='r')
        except Exception as e:
            border_file = open(st.path.border_log[:-4] + str(c) + '.log',
                               mode='w')
            break
        c += 1
    del c

    # border_file = open(st.path.border_before_log, mode='w')
    border_file.write(str(datetime.datetime.now()))
    border_file.write("\n\n")
    # endregion LOG_FILES

    link = dict()

    for host_id in instanse.ids:
        link[host_id] = 0

    near = None
    try:
        border = set()  # ids of border objects

        for host_id in instanse.ids:  # for each obj
            near = instanse.get_rel_of(host_id)  # get relative table of obj

            border_file.write(f"\n S[{host_id}];\t near:\n{near}\n")

            for row in near:          # looking for opponent on row host_id
                # if row[st.row.idn] in instanse.ids:
                if instanse.labels[host_id] != int(row[st.rel_of.label]):  # opponent found
                    border.add(int(row[st.rel_of.idn]))  # add opponent_id into border_dict
                    link[int(row[st.rel_of.idn])] += 1
                    border_file.write(f"S[{int(row[st.rel_of.idn])}] now border obj\n")
                    break  # stop looking for opponent
            else:  # if no opponent found
                import error_handler
                s = f"ERROR:: no border obj found :: border_selection ::\n" \
                    f"\thost_id:{host_id}; row[{host_id}]:{near}\n"
                error_handler.write(s, st)
                border_file.write(s)
            border_file.write(f"border: {border}\n")

        border_file.write("\n" + '='*50 + '\n')
        border_file.write(f"border: len:{len(border)}\n{border}")
        return border.copy(), link.copy()

    except Exception as e:
        import error_handler
        s = f"ERROR:: can't set border :: border_selection ::\n" \
            f"\thost_id:{host_id};\trow[{host_id}]:{near};\n" \
            f"\terror_msg: {e.args}"
        error_handler.write(s, st)
        border_file.write(s)
        return set(), dict()