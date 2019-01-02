"""
Here we would keep settings
"""

# TODO: settings:   move all settings to this file


class Rel_Of():

    idn = 0
    radius = 1
    label = 2


class DataDictionarySettings:

    def __init__(self):
        # default metric
        self.metric = 1  # "euclidean"  # Euclid

        # limit of diff in float data
        self.epsilon = 10 ** -7

        # project's path
        # self.file_path = None                                # "d:\\_NUU\\2018\\machine\\skulls"
        # self.datafile_path = None                            # "init_data\\skulls.csv"         #
        # self.labelfile_path = None                           # "init_data\\labels.csv"

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

        self.border = None
        self.noise = None
        self.shell = None
        self.groups = None
        self.ability = None

        # rel_of is m*3 table of required obj
        #    id  R    class
        #     0  0.7      0     # nearest obj
        #     7  1.5      0     # 2nd nearest obj
        #     9  1.59     1     # 3rd nearest obj
        #     ...   ...
        rel_of = {"id": 0, "radius": 1, "class": 2}

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
        # 5: "wminkowski",
        # 6: "seuclidean",
        # 7: "mahalanobis"
    }


class MetricClass:
    default_metric = 1
    metric_dict = {
        1: "euclidean",
        2: "manhattan",
        3: "chebyshev",
        4: "minkowski",
        # 5: "wminkowski",
        # 6: "seuclidean",
        # 7: "mahalanobis"
    }
    p = 2
    w = 1  # TODO: must be a n-size vector; n = features count


class ShellSelection:
    ...


class AllSettings:

    def __init__(self):
        self.metric = MetricClass()
        self.rel_of = Rel_Of()

        # region PATH
        self.DEFAULT_PATH = {
            # project path
            'project':      r'd:\_NUU\2018\machine\skulls',
            'dataset':      r'\init_data\skulls.csv',
            'label':        r'\init_data\labels.csv',
            # log path
            'border_log':   r'\output_data\border.log',
            'shell_log':    r'\output_data\shell.log',
            'error_log':    r'\output_data\shell4_error.data'
        }
        self.full_path = {
            'project': None,
            'dataset': None,
            'label': None,
            'border_log': None,
            'shell_log': None,
            'error_log': None
        }
        self.refactoring_path()
        # endregion PATH

    def refactoring_path(self):
        # PROJECT_PATH = self.DEFAULT_PATH['project']
        for key in self.DEFAULT_PATH.keys():
            if key != 'project':
                self.full_path[key] = self.DEFAULT_PATH['project'] + \
                                      self.DEFAULT_PATH[key]
            else:
                self.full_path[key] = self.DEFAULT_PATH[key]


