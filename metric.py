"""
There we will calculate distance
"""

# TODO: metric:     move distance function to this file
# TODO: metric:     add at least 7 top metrics

import validator

"""
Metrics intended for real-valued vector spaces:

  identifier	        class name	        args	        distance function
1 “euclidean”	        EuclideanDistance	                sqrt(sum((x - y)^2))
2 “manhattan”	        ManhattanDistance                   sum(|x - y|)
3 “chebyshev”	        ChebyshevDistance                   max(|x - y|)
4 “minkowski”	        MinkowskiDistance	p	            sum(|x - y|^p)^(1/p)
5 “wminkowski”	        WMinkowskiDistance	p, w	        sum(|w * (x - y)|^p)^(1/p)
6 “seuclidean”	        SEuclideanDistance	V	            sqrt(sum((x - y)^2 / V))
7 “mahalanobis”	        MahalanobisDistance	V or VI	        sqrt((x - y)' V^-1 (x - y))
"""


def distance(instance, host_id, other_id, metric=None):

    metric = validator.metric(metric)

    if metric == 1:
        return __euclidean_distance(instance, host_id, other_id)
    elif metric == 2:
        return 1


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
        r = sum((instance.df[host_id] - instance.df[other_id]) ** 2) ** 1 / 2
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


if __name__ == '__main__':
    ...

