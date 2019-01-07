""""""

import grouping
import pandas as pd
import numpy as np

import settings
import validator
import metric as metriclib
import border_selection
import error_handler
import noise_selection
import shell_selection

# TODO: data_dict: Change name of DataDict
# TODO: data_dict: move all init_variables to setting.py
# TODO: data_dict: move all possible functions to separate files for each
# TODO: data_dict: change getter/setters for more intuitive understanding
# TODO: data_dict: add more checker for datatype/valib numbers/etc
# TODO: data_dict: add more comments + correct __doc__ strings
# TODO: data_dict: create UPGRADE func additional to getter/setter

# TODO: data_dict\load_data:    unify input
# TODO: data_dict\load_data:    add ability to read labels from first/last column
# TODO: data_dict:


class DataDictionary(settings.DataDictionarySettings):

    def __init__(self):
        """init data"""
        super(DataDictionary, self).__init__()

        self.st = settings.AllSettings()    # Here we keep Settings for project

    def load_data(self,
                  *,
                  dataset_path=r"folder\with\Objects.csv",
                  dataset_file=r"full\path\to\the\Objects.csv",
                  target_file=r"full\path\to\the\Target.csv",
                  metric="Euclidean",  # Metric
                  p=2,  # metric
                  w=1,
                  normalize=0,
                  delimiter=None,
                  ):
        """ Loading dataset

        :param dataset_path: path to the folder with Objects.csv and Target.csv
                             Set this or next 2
        :param dataset_file: fullpath of Objects.csv file
        :param target_file:  fullpath of Target.csv file
        :param delimiter:    data delimiter in dataset
        :param metric:       Name or Number of metric
        :param p:            arg for some metrics
        :param w:            arg for some metrics
        :param normalize:    Name or Number of normalize algorithm
        :return:             True === OK / None === Some Error
        """

        # region VALIDATE ARGs

        # file path
        if dataset_path != r"folder\with\Objects.csv":
            self.st.path.dataset = dataset_path.rstrip('\\') + \
                                   '\\' + self.st.path.DEFAULT_PATH['dataset'].strip('\\\t\ ')
            self.st.path.label = dataset_path.rstrip('\\') + \
                                 '\\' + self.st.path.DEFAULT_PATH['label'].strip('\\\t\n ')

        if dataset_file != r"full\path\to\the\Objects.csv": self.st.path.dataset = dataset_file

        if target_file != r"full\path\to\the\Target.csv": self.st.path.label = target_file

        if not (validator.file_exist(self.st.path.dataset) and
                validator.file_exist(self.st.path.label)):
            print(f"ERROR:  on open {self.st.path.dataset} or {self.st.path.label}")
            return

        # metric
        metric = validator.metric(metric, self.st)
        p, w = validator.metric_pw(p, w, self.st)
        if not(p and w and metric):
            print(f"ERROR:   on metric: {metric} or p: {p} or w: {w}")
            return
        else:
            self.st.metric.default_metric = validator.metric(metric, self.st)
            self.st.metric.p = p
            self.st.metric.w = w

        # normalize
        if normalize:
            pass

        if delimiter is None:
            delimiter = self.delimiter

        # endregion VALIDATE

        # load data
        self.df = np.genfromtxt(self.st.path.dataset, delimiter=delimiter)
        self.labels = np.genfromtxt(self.st.path.label, delimiter=delimiter)

        self.__shape = self.df.shape
        self.ids = set(range(self.__shape[0]))
        self.sample = self.ids.copy()

        self.set_rel_table()
        return True

    # region REL_TABLE
    # REWORK rel_table.
    def get_rel_table(self):

        return self.rel

    def create_rel_table_old(self, metric, *_, p=None, w=None):
        # validate
        metric = validator.metric(metric, self.st)
        p, w = validator.metric_pw(p, w, self.st)

        # create a shape of relations table
        rel = np.zeros((self.__shape[0], self.__shape[0]))

        for host_id in self.ids:
            for other_idn in self.ids:
                rel[host_id][other_idn] = \
                    self.distance(host_id, other_idn)

        self.rel = rel

    def create_rel_table(self):
        """ Creates "near_table" of all objs

        3d array.
        1st index       === returns near_table. Include deleted ids
        2nd index       === returns row with info about <id>, <radius>, <label>. Exclude deleted ids
        3rd index       === returns one of <id>, <radius> or <label>

        :return:    rel_table
        """
        # <id>, <radius>, <label>
        rel_list = []
        for host_id in range(self.df.shape[0]):
            near = []
            # for other_id in range(self.df.shape[0]):
            for other_id in self.ids:   # this exclude deleted objs (# noise,)
                row = [other_id,
                       self.distance(host_id, other_id),
                       self.labels[other_id]]

                # rearrange as defined in settings.rel_of
                row[self.st.rel_of.idn], row[self.st.rel_of.radius], row[self.st.rel_of.label] = \
                    row[0], row[1], row[2]
                near.append(row)

            near = np.array(near)
            near = near[near[:, 1].argsort()]
            rel_list.append(near)

        rel = np.array(rel_list)
        self.rel = rel

    def set_rel_table(self, *_, rel_table=None, metric=None, p=None, w=None):
        """ Set or recreate self.rel

        :param rel_table:      rel_table with which you want replace self.rel_table
        :param metric:         metric (# Euclidean, manhattan...)
        :param p:              used in some metrics
        :param w:              used in some metrics
        :return:               None
        """

        if rel_table is None:
            if metric or p or w:
                metric = validator.metric(metric, self.st)
                p, w = validator.metric_pw(p, w, self.st)

                if metric != self.st.metric.default_metric:
                    self.st.metric.default_metric = metric
                    self.flag.metric = True
                if p != self.st.metric.p:
                    self.st.metric.p = p
                    self.flag.metric = True
                if w != self.st.metric.w:
                    self.st.metric.w = w
                    self.flag.metric = True

            self.create_rel_table()
        else:
            # TODO: need validation
            self.rel = rel_table

    def distance(self, host_id, other_id):
        return metriclib.distance(self, host_id, other_id)

    def get_rel_of_old(self, host_id, *_, rel_table=None):
        """Returns: 2d list with like [<other_id>, <r>, <other_class>]
                other_id    === other objects id
                r           === distance to other object
                other_class === other objects class
        """

        rel_of = []

        if rel_table is None:
            radiuslist = self.rel[host_id].tolist().copy()
        else:
            radiuslist = rel_table[host_id].tolist().copy()

        for other_id in self.ids:
            rel_of.append([other_id, radiuslist[other_id], self.labels[other_id]])

        rel_of = np.array(rel_of)

        # rel_of = rel_of[ sorted(list(self.ids)) ]
        own = np.where(rel_of[:, 0] == host_id)
        rel_of = np.delete(rel_of, (own[0][0]), axis=0)
        rel_of = rel_of[rel_of[:, 1].argsort()]
        return rel_of

    def get_rel_of(self, host_id):
            """ Return near_table for host_id.

            :param host_id:         any id of obj
            :return:                2d np.array like [<other_id>, <r>, <other_class>]
                    other_id    === other objects id
                    r           === distance to other object
                    other_class === other objects class
            """

            rel_of = self.rel[host_id]

            # Delete host_id from near_table
            own = np.where(rel_of[:, 0] == host_id)
            rel_of = np.delete(rel_of, (own[0][0]), axis=0)

            return rel_of

    def get_nearest_opponent(self, host_id):
            """Returns: 1d array like [<r>, <opponent_id>, <opponent_class>]
                    r              === distance to other object
                    opponent_id    === other objects id
                    opponent_class === other objects class
            """

            near = self.get_rel_of(host_id)

            for row in near:
                if self.labels[host_id] != row[self.st.rel_of.label]:
                    return row
            else:
                s = f"ERROR:     dd.get_nearest_opponent(host_id={host_id})\n" \
                    f"\tnearest_opponent not found:: rel_of({host_id})={near}"
                error_handler.write(s, self.st)
            return None

    # endregion REL_TABLE

    # region BORDER
    def set_link(self, link=None):

        if link:
            self.link = link

    def get_link(self, host_id=None):
        if host_id is None:
            return self.link.copy()
        else:
            return self.link[host_id]

    def create_border(self):
        border, link = border_selection.get_border(self)
        self.border = border
        self.link = link

    def get_border(self, *_, recreate=False):
        if recreate: self.create_border()
        return self.border

    def set_border(self, border=None):

        if border is not None:
            self.border = border
        else:
            self.border = self.get_border(recreate=True)

    # endregion BORDER

    # region NOISE

    def set_noise(self, *_, noise=None, recreate=False):
        if recreate or noise is None:
            self.noise = noise_selection.get_noise(self, self.st)
        else:
            self.noise = noise

    def get_noise(self, requested_id=None, border=None, *_, recreate=False):
        """ identify NOISE objects

        :param requested_id:    -*check requested_id is noise or not (optional)
        :param border:          - IDs of border obj
        :return:                - 1) set of noise obj's id_number //
                                  2) True/False (if id given)*
        """

        if recreate or self.noise is None:
            self.set_noise(recreate=True)
        return self.noise  # EoF get_noise()

    # endregion NOISE

    # region SHELL
    def get_shell(self, *_, recreate=False):
        """ identify SHELL objects """
        if recreate:
            self.create_shell()
        return self.shell

    def set_shell(self, shell=None, *_, recreate=False):
        if recreate or shell is None:
            self.create_shell()
        if shell:
            self.shell = shell

    def create_shell(self):
        self.shell = shell_selection.get_shell(self, st=self.st)
    # endregion SHELL

    # region GROUP
    def create_group(self):
        self.groups = grouping.get_groups(self, self.st)

    def set_groups(self, groups=None, *_, recreate=False):
        if recreate or groups is None:
            self.create_group()
        if groups:
            self.groups = groups

    def get_groups(self, recreate=False):

        if recreate or self.groups is None:
            self.create_group()

        return self.groups

    # endregion GROUP

    def get_ability(self):
        import ability
        self.ability = ability.get_compactness(self)
        return self.ability

    def get_standard(self, groups):
        import standard_selection
        return standard_selection.get_standard(self)

