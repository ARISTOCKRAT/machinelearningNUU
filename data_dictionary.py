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

        self.st = settings.AllSettings()

        # ************* VARIABLES ***************
        # ************/ VARIABLES /************** #

    def load_data(self,
                  datafile_path="init_data\\skulls.csv",
                  labelfile_path="init_data\\labels.csv",
                  *,
                  metric=1):
        """loading data set"""

        from numpy import genfromtxt

        self.path = "d:\\_NUU\\2018\\machine\\skulls"

        self.file_path = datafile_path
        self.df = genfromtxt(datafile_path, delimiter=",")
        self.labels = genfromtxt(labelfile_path, delimiter=",")
        self.shape = self.df.shape
        self.row_count = self.shape[0]
        self.col_count = self.shape[1]
        self.ids = set(range(self.df.shape[0]))

        self.set_rel_table(metric=metric)
        # self.rel = self.get_rel_table(metric=self.metric)  # set is enough

    def get_rel_table(self, metric=1, *_, rel_table=None, recreate=False):

        # if recreate:
        #
        #     self.create_rel_table(metric=metric, p=2, w=1)
        #     # validate
        #     metric = validator.metric(metric)
        #
        #     rel = np.arange(self.row_count**2).reshape((self.row_count, self.row_count))
        #
        #     for host_id in self.ids:
        #         line = []
        #         for other_idn in self.ids:
        #             rel[host_id][other_idn] = \
        #                 self.distance(host_id, other_idn, metric=metric, rel_table=rel_table)
        #
        # return rel
        return self.rel

    def create_rel_table(self, metric=1, *_, p=None, w=None):
        # validate
        metric = validator.metric(metric, self.st)
        p, w = validator.metric_pw(p, w, self.st)

        # create a shape of relations table
        rel = np.zeros((self.row_count, self.row_count))

        for host_id in self.ids:
            for other_idn in self.ids:
                rel[host_id][other_idn] = \
                    self.distance(host_id, other_idn, self.st, metric=metric, p=p, w=p)

        self.rel = rel

    def set_rel_table(self, *_, rel_table=None, metric=1, p=None, w=None):
        """
        :param rel_table:      # rel_table with which you want replace self.rel_table
        :param metric:         # by default 1 ==> Euclidean
        :return:               # None
        """
        metric = validator.metric(metric, self.st)

        if rel_table is None:
            self.create_rel_table(metric=metric, p=p, w=w)
            # self.rel = self.get_rel_table(metric=metric, p=2, w=1, recteate=True)
        else:
            self.rel = rel_table

    def distance(self, host_id, other_id, st, *, metric=None, p=None, w=None, rel_table=None):

        if rel_table is None:
            return metriclib.distance(
                self, host_id, other_id, st=st, metric=metric, p=p, w=w
            )
        else:
            return metriclib.distance(
                self, host_id, other_id, st=st, metric=metric, p=p, w=w,
                rel_table=rel_table
            )

    def get_rel_of(self, host_id, *_, rel_table=None):
        """Returns: 2d list with like [<other_id>, <r>, <other_class>]
                other_id    === other objects id
                r           === distance to other object
                other_class === other objects class
        """

        rel_of = None
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

    def get_nearest_opponent(self, host_id, *_, rel_table=None):
            """Returns: list like [<r>, <opponent_id>, <opponent_class>]
                    r              === distance to other object
                    opponent_id    === other objects id
                    opponent_class === other objects class
            """

            rel_of = self.get_rel_of(host_id)

            for row in rel_of:
                if self.labels[host_id] != row[2]:
                    return row
            else:
                s = f"ERROR:     dd.get_nearest_opponent(host_id={host_id})\n" \
                    f"\tnearest_opponent not found:: rel_of({host_id})={rel_of}"
                error_handler.write(s)
            return None

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
            self.noise = noise_selection.get_noise(self)
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
        self.shell = shell_selection.get_shell(self)
    # endregion SHELL

    def set_groups(self, groups=None):

        if groups is None:
            self.groups = grouping.get_groups(self, self.st)
        else:
            self.groups = groups

    def get_groups(self):
        return self.groups

    def get_ability(self):
        import ability
        self.ability = ability.get_compactness(self)
        return self.ability

    def get_standard(self, groups):
        import standart_selection
        return standart_selection.get_standart(self, groups)

