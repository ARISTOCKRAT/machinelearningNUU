"""
Here we would keep settings
"""

# TODO: settings:   move all settings to this file


class RelOf:

    idn = 0
    radius = 1
    label = 2


class PathSettings:
    # project path
    project = r'd:\_NUU\2018\machine\skulls'
    dataset = r'\init_data\skulls.csv'
    label = r'\init_data\labels.csv'

    # log path
    border_log = r'\output_data\border.log'
    shell_log = r'\output_data\shell.log'
    error_log = r'\output_data\error.log'
    binary_log = r'\output_data\group_binary.log'
    standart_log = r'\output_data\standart_selection.log'

    # default path
    DEFAULT_PATH = {
        # project path
        'project': r'd:\_NUU\2018\machine\skulls',
        'dataset': r'\init_data\skulls.csv',
        'label': r'\init_data\labels.csv',
        # log path
        'border_log': r'\output_data\border.log',
        'shell_log': r'\output_data\shell.log',
        'error_log': r'\output_data\error.log',
        'binary_log': r'\output_data\group_binary.log',
        'standart_log': r'\output_data\standart_selection.log',
    }

    def __init__(self):
        PathSettings.refactoring_path()

    #
    @staticmethod
    def refactoring_path(project_path=None):
        if project_path is None: project_path = PathSettings.DEFAULT_PATH['project']

        # project path
        PathSettings.dataset = project_path + PathSettings.DEFAULT_PATH['dataset']
        PathSettings.label = project_path + PathSettings.DEFAULT_PATH['label']

        # log path
        PathSettings.border_log = project_path + PathSettings.DEFAULT_PATH['border_log']
        PathSettings.shell_log = project_path + PathSettings.DEFAULT_PATH['shell_log']
        PathSettings.error_log = project_path + PathSettings.DEFAULT_PATH['error_log']
        PathSettings.binary_log = project_path + PathSettings.DEFAULT_PATH['binary_log']
        PathSettings.standart_log = project_path + PathSettings.DEFAULT_PATH['standart_log']


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


class MetricSettings:
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
        self.metric = MetricSettings()
        self.rel_of = RelOf()
        self.path = PathSettings()
        # self.path.refactoring_path()


