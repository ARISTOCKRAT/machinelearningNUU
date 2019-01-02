"""
There we will calculate distance
"""

# done: metric:     move distance function to this file
# done: metric:     add at least 7 top metrics
# TODO: metric:     add new popular metrics
# TODO: metric:     fix, select def metric (не выбирается по умолчанию)


import validator
import settings

"""
Metrics intended for real-valued vector spaces:

  identifier	        class name	        args	        distance function
+ “euclidean”	        EuclideanDistance	                sqrt(sum((x - y)^2))
+ “manhattan”	        ManhattanDistance                   sum(|x - y|)
+ “chebyshev”	        ChebyshevDistance                   max(|x - y|)
+ “minkowski”	        MinkowskiDistance	p	            sum(|x - y|^p)^(1/p)
+ “wminkowski”	        WMinkowskiDistance	p, w	        sum(|w * (x - y)|^p)^(1/p)
6 “seuclidean”	        SEuclideanDistance	V	            sqrt(sum((x - y)^2 / V))
7 “mahalanobis”	        MahalanobisDistance	V or VI	        sqrt((x - y)' V^-1 (x - y))
"""


# rel_table WILL NOT PROVIDE as arg
# def distance(instance, host_id, other_id, metric=None, *, p=2, w=1, rel_table=None, rel_table=None):
def distance(instance, host_id, other_id, st, *, metric=None, p=2, w=1, rel_table=None):

    # TODO: +add rel_table validator
    # if rel_table is None:
    rel_table = instance.rel

    metric = validator.metric(metric, st)

    if settings.metric.metric_dict[metric] == 'euclidean':
        return __euclidean_distance(instance, host_id, other_id)

    elif settings.metric.metric_dict[metric] == 'chebyshev':
        return __chebyshev_distance(instance, host_id, other_id)

    elif settings.metric.metric_dict[metric] == 'manhattan':
        return __manhattan_distance(instance, host_id, other_id)

    # w - MUST BE A VECTOR ??
    elif settings.metric.metric_dict[metric] == 'minkowski':
        return __minkowski_distance(instance, host_id, other_id, p, w)

    # w - MUST BE A VECTOR ??
    elif settings.metric.metric_dict[metric] == 'wminkowski':
        return __minkowski_distance(instance, host_id, other_id, p, w)


def __euclidean_distance(instance, host_id, other_id):
    """
    Calculates distance btw 2 obj using Euclidean metric sys

    :param instance:        # instance of DataDictionary for extracting obj features
    :param host_id:         # identifier of obj1
    :param other_id:        # identifier of obj2
    :return:                # distance btw obj1 & obj2
    """

    r = None
    try:
        r = sum((instance.df[host_id] - instance.df[other_id]) ** 2) ** .5
    except Exception as e:
        import error_handler
        s = f"ERROR:\t on calculate distance:: Euclidean ::" \
            f"\n\thost_id:({host_id}); other_id:{other_id}; error:{e.args}"
        error_handler.write(s)
    return r


def __minkowski_distance(instance, host_id, other_id, p, w):
    """
    Calculates distance btw 2 obj using Minkowski's metric sys

    :param instance:        # instance of DataDictionary for extracting obj features
    :param host_id:         # identifier of obj1
    :param other_id:        # identifier of obj2
    :return:                # distance btw obj1 & obj2
    """

    r = None
    print(f"host:{instance.df[host_id]}; oth:{instance.df[other_id]}; p={p}")
    try:
        r = sum(
            abs(
                w * (instance.df[host_id] - instance.df[other_id])
               ) ** p
               ) ** (1 / p)
    except Exception as e:
        import error_handler
        s = f"ERROR:\t on calculate distance:: Euclidean ::" \
            f"\n\thost_id:({host_id}); other_id:{other_id}; error:{e.args}"
        error_handler.write(s)
    return r


def __chebyshev_distance(instance, host_id, other_id):
    """
    Calculates distance btw 2 obj using chebyshev's metric sys

    :param instance:        # instance of DataDictionary for extracting obj features
    :param host_id:         # identifier of obj1
    :param other_id:        # identifier of obj2
    :return:                # distance btw obj1 & obj2
    """

    r = None
    try:
        x = instance.df[host_id]
        y = instance.df[other_id]
        return max(abs(x - y))
    except Exception as e:
        import error_handler
        s = f"ERROR:\t on calculate distance:: __chebyshev_distance ::" \
            f"\n\thost_id:({host_id}); other_id:{other_id}; error:{e.args}"
        error_handler.write(s)
    return r


def __manhattan_distance(instance, host_id, other_id):
    """
    Calculates distance btw 2 obj using Manhattan metric sys

    :param instance:        # instance of DataDictionary for extracting obj features
    :param host_id:         # identifier of obj1
    :param other_id:        # identifier of obj2
    :return:                # distance btw obj1 & obj2
    """

    r = None
    try:
        x = instance.df[host_id]
        y = instance.df[other_id]
        return sum(abs(x - y))
    except Exception as e:
        import error_handler
        s = f"ERROR:\t on calculate distance:: __manhattan_distance ::" \
            f"\n\thost_id:({host_id}); other_id:{other_id}; error:{e.args}"
        error_handler.write(s)
    return r


if __name__ == '__main__':
    ...

