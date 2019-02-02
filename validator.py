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


def boolean(some_bool):
    # TODO: create validator
    return some_bool


def normalize(instance, method_name):

    if method_name:

        # INT
        if type(method_name) is int:
            if instance.st.normalize.normalize_dict.get(method_name) is None:
                error_handler.write(f"ERROR:\t unresolved method_name:: continue working as default::"
                                    f"\n\tnormalize method({method_name}) is {type(method_name)}")
                return instance.st.normalize.default_normalize
            else:
                return method_name

        # FLOAT
        elif type(method_name) is float:
            return normalize(instance, int(method_name))

        # STR
        elif type(method_name) is str:
            method_name = method_name.lower()
            for item in instance.st.normalize.normalize_dict.items():
                if method_name == item[1]:
                    return item[0]
            else:  # if no matches
                error_handler.write(f"ERROR:\t out of range:: continue working as default::"
                                    f"\n\tmethod name({method_name}) is {type(method_name)}")
                return instance.st.normalize.default_normalize

        # LIST or TUPLE
        elif (type(method_name) is list or type(method_name) is tuple) and method_name:
            return normalize(instance, method_name[0])

        # DICT or SET
        elif type(method_name) is dict:
            for el in method_name.items():
                return normalize(instance, el[1])
        elif type(method_name) is set:
            for el in method_name:
                return normalize(instance, el)

        # UNKNOWN type of value
        else:
            error_handler.write(f"ERROR:\t unresolved type of value::\n\t"
                                f"method name ({method_name}) is {type(method_name)}")
            return instance.st.normalize.default_normalize
    else:
        if method_name is None:
            return instance.st.normalize.default_normalize

    return instance.st.normalize.default_normalize

