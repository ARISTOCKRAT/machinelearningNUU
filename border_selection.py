
# TODO: border_selection: more algorithms for border selection


def get_border(instanse):
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

            for rel_of in near:          # looking for opponent on rel_of host_id
                if instanse.labels[host_id] != rel_of[2]:  # opponent found
                    border.add(int(rel_of[0]))  # add opponent_id into border_dic
                    link[int(rel_of[0])] += 1
                    break  # stop looking for opponent
            else:  # if no opponent found
                import error_handler
                s = f"ERROR:: no border obj found :: border_selection ::\n" \
                    f"\thost_id:{host_id}; rel_of[{host_id}]:{near}\n"
                error_handler.write(s)

        return border.copy(), link

    except Exception as e:
        import error_handler
        s = f"ERROR:: can't set border :: border_selection ::\n" \
            f"\thost_id:{host_id};\trel_of[{host_id}]:{near};\n" \
            f"\terror_msg: {e.args}"
        return set(), dict()