"""
Here we would keep settings
"""

# TODO: settings:   move all settings to this file


class rel_of():

    idn = 0
    radius = 1
    label = 2


class DataDictionarySettings:

    def __init__(self):
        # default metric
        self.metric = 1  # "euclidean"  # Euclid

        # limit of diff in float data
        self.epsilon = 10 ** -7

        # projects path
        self.file_path = None                                # "d:\\_NUU\\2018\\machine\\skulls"
        self.datafile_path = None                            # "init_data\\skulls.csv"         #
        self.labelfile_path = None                           # "init_data\\labels.csv"

        self.df = None
        self.labels = None
        self.ids = None
        self.row_count = None
        self.col_count = None
        self.shape = None
        self.rel = None
        self.border = None

        self.near_table = None
        self.link = None
        self.path = None

        self.shell = None
        self.groups = None
        self.ability = None

        # rel_of is m*3 table of required obj
        #    id  R    class
        #     0  0.7      0     # nearest obj
        #     7  1.5      0     # 2nd nearest obj
        #     9  1.59     1     # 3rd nearest obj
        #     ...   ...
        # self.rel_of = {"id": 0, "radius": 1, "class": 2}

        # delimiter
        # self.load_data = {"delimiter": ","}


class ErrorHandler:
    error_file_path = r"d:\_NUU\2018\machine\skulls\output_data\error.log"


class metric:
    default_metric = 1
    metric_dict = {
        1: "euclidean",
        2: "manhattan",
        3: "chebyshev",
        4: "minkowski",
        5: "wminkowski",
        6: "seuclidean",
        7: "mahalanobis"
    }