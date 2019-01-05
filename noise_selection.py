"""
There we will select shell obj
"""

# TODO: noise_selection:    add more algorithms

'''
def get_noise(instance, requested_id=None, border=None):
    """ identify NOISE objects

        :param instance:    -
        :param data_dict:   - data in own dictionary form.
        :param border:      - IDs of border obj
        :return:            - set of noise obj's id_number
    """

    if border is None:
        border = instance.get_border()

    noise = set()

    if requested_id is None:
        for host_id in border:
            K = instance.get_link(host_id)

            # Calc L (count of friendly within R = distance to nearest opponent)
            L = 0
            near = instance.get_rel_of(host_id)
            for rel_of in near:
                if instance.labels[host_id] == int(rel_of[2]):
                    L += 1
                else:
                    break

            try:
                if L == 0 or K / L > 1:
                    noise.add(host_id)
            except Exception as e:
                print(f"NOISE ERROR:   id:{host_id:4} K={K:3} L={L:3}\t{e.args}")
                print(f"rel_of({host_id}: {instance.get_rel_of(host_id)})")
    else:
        host_id = requested_id
        K = instance.get_link(host_id)
        L = 0
        near = instance.get_rel_of(host_id)
        for rel_of in near:
            if instance.labels[host_id] == int(rel_of[2]):
                L += 1
            else:
                break

        try:
            if K / L > 1:
                return True
        except Exception as e:
            print(f"NOISE ERROR:   id:{host_id:4} K={K:3} L={L:3}\t{e.args}")

        return False

    return noise.copy()  # EoF get_noise()
'''


def get_noise(instance, st, requested_id=None, border=None):
    """ identify NOISE objects

    :param instance:        - instance of the DD
    :param requested_id:    -*check requested_id is noise or not (optional)
    :param border:          - IDs of border obj
    :return:                - 1) set of noise obj's id_number //
                              2) True/False (if id given)*
    """

    if border is None:
        border = instance.border

    noise = set()

    if requested_id is None:
        for host_id in border:
            K = instance.get_link(host_id)

            # Calc L (count of friendly within R = distance to nearest opponent)
            L = 0
            near = instance.get_rel_of(host_id)
            for rel_of in near:
                if instance.labels[host_id] == int(rel_of[st.rel_of.label]):
                    L += 1
                else:
                    break

            if K > L:
                noise.add(host_id)

    else:
        host_id = requested_id
        K = instance.get_link(host_id)
        L = 0
        near = instance.get_rel_of(host_id)
        for rel_of in near:
            if instance.labels[host_id] == int(rel_of[st.rel_of.label]):
                L += 1
            else:
                break

        if K > L:
            return True
        return False

    return noise.copy()  # EoF get_noise()

