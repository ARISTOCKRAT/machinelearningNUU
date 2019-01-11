"""
Here we would keep settings
"""

# TODO: settings:   move all settings to this file


class RelOf:

    idn = 0
    radius = 1
    label = 2


class Counters:
    border = 1


class PathSettings:
    # project path
    project = r'd:\_NUU\2018\machine\skulls'
    dataset_path = project + r'\init_data\skull'
    dataset = project + r'\Objects.csv'
    label = project + r'\Target.csv'

    # log path
    border_log = r'\output_data\border.log'
    border_after_log = r'\output_data\border.log'
    normalize_log = r'\output_data\normalize.log'
    noise_log = r'\output_data\noise.log'
    shell_log = r'\output_data\shell.log'
    error_log = r'\output_data\error.log'
    binary_log = r'\output_data\group_binary.log'
    standard_log = r'\output_data\standard_selection.log'

    # default path
    DEFAULT_PATH = {
        # project path
        'project': r'd:\_NUU\2018\machine\skulls',
        'dataset': r'\Objects.csv',
        'label': r'\Target.csv',
        # log path
        'border_log': r'\output_data\border.log',
        'border_after_log': r'\output_data\border_after_noise.log',
        'normalize_log': r'\output_data\normalize.log',
        'noise_log': r'\output_data\noise.log',
        'shell_log': r'\output_data\shell.log',
        'error_log': r'\output_data\error.log',
        'binary_log': r'\output_data\group_binary.log',
        'standard_log': r'\output_data\standard_selection.log',
    }

    def __init__(self):
        PathSettings.refactoring_path()

    #
    @staticmethod
    def refactoring_path(project_path=None, *, dataset=None, label=None):
        # project path
        # if project_path is None: project_path = PathSettings.DEFAULT_PATH['project']
        # PathSettings.label = project_path + PathSettings.DEFAULT_PATH['label']

        project_path = project_path if project_path else PathSettings.DEFAULT_PATH['project']
        PathSettings.dataset = dataset if dataset else project_path + PathSettings.DEFAULT_PATH['dataset']
        PathSettings.label = label if label else project_path + PathSettings.DEFAULT_PATH['label']

        # log path
        PathSettings.border_log = project_path + PathSettings.DEFAULT_PATH['border_log']
        PathSettings.border_after_log = project_path + PathSettings.DEFAULT_PATH['border_after_log']
        PathSettings.noise_log = project_path + PathSettings.DEFAULT_PATH['noise_log']
        PathSettings.normalize_log = project_path + PathSettings.DEFAULT_PATH['normalize_log']
        PathSettings.shell_log = project_path + PathSettings.DEFAULT_PATH['shell_log']
        PathSettings.error_log = project_path + PathSettings.DEFAULT_PATH['error_log']
        PathSettings.binary_log = project_path + PathSettings.DEFAULT_PATH['binary_log']
        PathSettings.standard_log = project_path + PathSettings.DEFAULT_PATH['standard_log']


class FlagSettings:
    metric = False

    @staticmethod
    def changed():
        c = set()
        if FlagSettings.metric:
            c.add('metric')
        return c


class DataDictionarySettings:

    def __init__(self):

        self.epsilon = 10 ** -7  # may be it will be useful somewhere

        self.df = None
        self.labels = None
        self.ids = None
        self.sample = None

        self.__shape = None
        self.rel = None
        self.near_table = None

        self.link = None
        self.border = None
        self.noise = None
        self.shell = None
        self.groups = None
        self.ability = None
        self.standard = None

        # load_data
        self.delimiter = ','
        # self.load_data = {"delimiter": ","}

        # FLAGS
        self.flag = FlagSettings()


class MetricSettings:
    default_metric = 1
    metric_dict = {
        1: "euclidean",
        2: "manhattan",
        3: "chebyshev",
        4: "minkowski",
        5: "hemming",
        # 5: "wminkowski",
        # 6: "seuclidean",
        # 7: "mahalanobis"
    }
    p = 2
    w = 1  # TODO: must be a n-size vector; n = features count


class NormalizeSettings:
    default_normalize = 1
    normalize_dict = {
        1: "method1",
        2: "method2",
        3: "method3",
        4: "method4",
    }


class AllSettings:

    def __init__(self):
        self.metric = MetricSettings()
        self.rel_of = RelOf()
        self.path = PathSettings()
        self.counter = Counters()
        self.normalize = NormalizeSettings()

