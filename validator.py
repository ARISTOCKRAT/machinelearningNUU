"""Here we validate values"""

# TODO: validate GROUPS

import error_handler


# validate the metric value
def metric(metric_name, st):
    # done: use st from DD, don't import
    # import settings

    if metric_name:

        # INT
        if type(metric_name) is int:
            if st.metric.metric_dict.get(metric_name) is None:
                error_handler.write(f"ERROR:\t unresolved metric_name:: continue working as default::"
                                    f"\n\tmetric type({metric_name}) is {type(metric_name)}")
                return st.metric.default_metric
            else:
                return metric_name

        # FLOAT
        elif type(metric_name) is float:
            return metric(int(metric_name), st)

        # STR
        elif type(metric_name) is str:
            metric_name = metric_name.lower()
            # for item in settings.metric.metric_dict.items():
            for item in st.metric.metric_dict.items():
                if metric_name == item[1]:
                    return item[0]
            else:  # if no matches
                error_handler.write(f"ERROR:\t out of range:: continue working as default::"
                                    f"\n\tmetric type({metric_name}) is {type(metric_name)}")
                return st.metric.default_metric

        # LIST or TUPLE
        elif (type(metric_name) is list or type(metric_name) is tuple) and metric_name:
            return metric(metric_name[0], st)

        # DICT or SET
        elif type(metric_name) is dict:
            for el in metric_name.items():
                return metric(el[1], st)
        elif type(metric_name) is set:
            for el in metric_name:
                return metric(el, st)

        # UNKNOWN type of value
        else:
            error_handler.write(f"ERROR:\t unresolved type of value::\n\t"
                                f"metric type({metric_name}) is {type(metric_name)}")
    else:
        if metric_name is None:
            return st.metric.default_metric
        error_handler.write(f"ERROR:\t invalid value:: continue working as default::\n\t"
                            f"metric type({metric_name}) is {type(metric_name)}")

    return st.metric.default_metric


def metric_pw(p, w, st):
    """ Here we should check p and w

    :param p:   === p (# minkowski)
    :param w:   === w (# minkowski, seuclidean)
    :param st:  === instance of settings
    :return:    === tuple of 2 elements p, w
    """
    # TODO: checker
    # p = st.metric.p
    # w = st.metric.w
    return p, w


# validate the rel table size etc
def rel_table(rel_table_obj):
    import numpy as np

    if type(rel_table_obj) is not np.array:
        return None


def file_exist(file_path):
    path = None
    try:
        f = open(file_path, mode='r')
        f.close()
    except Exception as e:
        msg = f"ERROR:   on open file by path {path}. msg:{e.args}"
        error_handler.write(msg)
        return False
    else:
        return True

