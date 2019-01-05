
# TODO: border_selection: more algorithms for border selection


def get_border(instanse, st):
    """ identify BORDER objects

    :param data_dict:   - data in own dictionary form.
    :return:            - set of border obj's id_number
    """

    link = dict()

    for host_id in instanse.ids:
        link[host_id] = 0

    near = None
    try:
        border = set()  # ids of border objects

        for host_id in instanse.ids:  # for each obj
            near = instanse.get_rel_of(host_id)  # get relative table of obj

            for row in near:          # looking for opponent on row host_id
                # if row[st.row.idn] in instanse.ids:
                if instanse.labels[host_id] != int(row[st.rel_of.label]):  # opponent found
                    border.add(int(row[st.rel_of.idn]))  # add opponent_id into border_dict
                    link[int(row[st.rel_of.idn])] += 1
                    break  # stop looking for opponent
            else:  # if no opponent found
                import error_handler
                s = f"ERROR:: no border obj found :: border_selection ::\n" \
                    f"\thost_id:{host_id}; row[{host_id}]:{near}\n"
                error_handler.write(s, st)

        return border.copy(), link.copy()

    except Exception as e:
        import error_handler
        s = f"ERROR:: can't set border :: border_selection ::\n" \
            f"\thost_id:{host_id};\trow[{host_id}]:{near};\n" \
            f"\terror_msg: {e.args}"
        error_handler.write(s, st)
        return set(), dict()