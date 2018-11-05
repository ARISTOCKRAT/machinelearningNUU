""""""

import grouping
import pandas as pd
import numpy as np

import settings

# TODO: data_dict: Change name of DataDict
# TODO: data_dict: move all init_variables to setting.py
# TODO: data_dict: move all possible functions to separate files for each
# TODO: data_dict: change getter/setters for more intuitive understanding
# TODO: data_dict: add more checker for datatype/valib numbers/etc
# TODO: data_dict: add more comments + correct __doc__ strings

# TODO: data_dict\load_data:    unify input
# TODO: data_dict\load_data:    add ability to read labels from first/last column
# TODO: data_dict:


class DataDictionary(settings.DataDictionarySettings):

    def __init__(self):
        """init data"""
        super(DataDictionary, self).__init__()

        # ************* VARIABLES ***************
        # ************/ VARIABLES /************** #

    def load_data(self,
                  datafile_path="init_data\\skulls.csv",
                  labelfile_path="init_data\\labels.csv", *_):
        """loading data set"""

        from numpy import genfromtxt

        self.path = "d:\\_NUU\\2018\\machine\\skulls"

        self.file_path = datafile_path
        # self.df = pd.read_csv(file_path)
        self.df = genfromtxt(datafile_path, delimiter=",")
        self.labels = genfromtxt(labelfile_path, delimiter=",")
        self.shape = self.df.shape
        self.row_count = self.shape[0]
        self.col_count = self.shape[1]
        self.ids = set(range(self.df.shape[0]))

        self.set_rel_table()
        self.rel = self.get_rel_table(metric=self.metric)

    def get_rel_table(self, metric=None):
        """ CREATE RELATIVE TABLE FOR EACH OBJECT ******************************
            rel[ id1, id2, ... idm
            id1,   0, 1.7, ... 12.2
            ...  ...  ...  ... ...
            idm  1.2, 1.5, ... 0  ]
        ******************************************************************** """

        rel = np.arange(self.row_count**2).reshape((self.row_count, self.row_count))

        for host_id in self.ids:
            line = []
            for other_idn in self.ids:
                rel[host_id][other_idn] = self.distance(host_id, other_idn, metric)

        return rel

    def set_rel_table(self, *_, rel_table=None, metric=None):
        """
        :param rel_table:      # rel_table with which you want replace self.rel_table
        :param metric:         # by default Euclidean
        :return:               # None
        """
        if metric is None:

        if not rel_table:
            self.rel = self.get_rel_table(self.metric)
        else:
            self.rel = rel_table

    def distance(self, host_id, other_id, metric=0):
        """Calculate distance with honor of metric"""
        r = 0  # distance
        if metric == 0:  # euclidean
            r = sum((self.df[host_id] - self.df[other_id])**2 ) ** 1/2

        return r

    def get_rel_of(self, host_id, *_, rel_table=None):
        """Returns: 2d list with like [<r>, <other_id>, <other_class>]
                r           === distance to other object
                other_id    === other objects id
                other_class === other objects class
        """

        rel_of = None
        rel_of = []
        radiuslist = self.rel[host_id].tolist().copy()
        for other_id in self.ids:
            rel_of.append([other_id, radiuslist[other_id], self.labels[other_id]])

        rel_of = np.array(rel_of)
        
        # rel_of = rel_of[ sorted(list(self.ids)) ]
        own = np.where(rel_of[:, 0] == host_id)
        rel_of = np.delete(rel_of, (own[0][0]), axis=0)
        rel_of = rel_of[rel_of[:, 1].argsort()]
        return rel_of

    def set_link(self, link=None):
        """ CALCULATE K = number of links ***************************************
            data_dict[<id_number>]            === dict with all data about object
            data_dict[<id_number>]['link']    === number of border links
                                                = (для скольких этот объект является граничным)
        ************************************************************************* """

        # if link is None:
        #     self.link = dict()
        #
        #     for host_id in self.ids:
        #         self.link[host_id] = 0
        #
        #     for host_id in self.ids:
        #         near = self.get_rel_of(host_id)
        #
        #         for rel_of in near:
        #             if self.labels[host_id] != rel_of[2]:
        #                 self.link[int(rel_of[0])] += 1
        #                 break
        # else:
        #     self.link = link

        ...
        # EoF set_link(self, link=None):

    def get_link(self, host_id=None):
        if host_id is None:
            return self.link.copy()
        else:
            return self.link[host_id]

    # /end/ def get_link(self, host_id=None):

    def get_border(self):
        """ identify BORDER objects

        :param data_dict:   - data in own dictionary form.
        :return:            - set of border obj's id_number
        """

        self.link = dict()

        for host_id in self.ids:
            self.link[host_id] = 0

        near = None
        try:
            border = set()  # ids of border objects

            for host_id in self.ids:  # for each obj
                near = self.get_rel_of(host_id)  # get relative table of obj

                for rel_of in near:          # looking for opponent on rel_of host_id
                    if self.labels[host_id] != rel_of[2]:  # opponent found
                        border.add(int(rel_of[0]))  # add opponent_id into border_dic
                        self.link[int(rel_of[0])] += 1
                        break  # stop looking for opponent
                else:  # if no opponent found
                    print(f"no opponent found for {host_id}")

            return border.copy()

        except Exception as e:
            print(f"host_id:{host_id};\tnear:{near};\n")
                  # f"len near:{self.link}")
            print(f'data_dict contents not valid data. {e.args}')
            return set()

    def set_border(self, border=None):

        if border is not None:
            self.border = border
        else:
            self.border = self.get_border()

    def get_noise(self, requested_id=None, border=None):
        """ identify NOISE objects

            :param data_dict:   - data in own dictionary form.
            :param border:      - IDs of border obj
            :return:            - set of noise obj's id_number
        """

        if border is None:
            border = self.border

        noise = set()

        if requested_id is None:
            for host_id in border:
                K = self.get_link(host_id)

                # Calc L (count of friendly within R = distance to nearest opponent)
                L = 0
                near = self.get_rel_of(host_id)
                for rel_of in near:
                    if self.labels[host_id] == int(rel_of[2]):
                        L += 1
                    else:
                        break

                try:
                    if L == 0 or K/L > 1:
                        noise.add(host_id)
                except Exception as e:
                    print(f"NOISE ERROR:   id:{host_id:4} K={K:3} L={L:3}\t{e.args}")
                    print(f"rel_of({host_id}: {self.get_rel_of(host_id)})")
        else:
            host_id = requested_id
            K = self.get_link(host_id)
            L = 0
            near = self.get_rel_of(host_id)
            for rel_of in near:
                if self.labels[host_id] == int(rel_of[2]):
                    L += 1
                else:
                    break

            try:
                if K / L > 1:
                    return True
            except Exception as e:
                print(f"NOISE ERROR:   id:{host_id:4} K={K:3} L={L:3}\t{e.args}")

            return False

        return noise.copy()  # EoF get_noise()

    def get_shell(self):
        """ identify SHELL objects
        :param data_dict:   - data in own dictionary form.
        :return:            - set of shell obj's id_number
        """
        import shell_selection

        shell = shell_selection.get_shell(self)

        return shell  # EoF get_shell

    def set_shell(self, shell=None):
        if shell is None:
            shell = self.get_shell()

        self.shell = shell

    def set_groups(self, groups=None):
        import settings as st
        if groups is None:
            self.groups = grouping.get_groups(self, st)
        else:
            self.groups = groups

    def get_groups(self):
        return self.groups

    def get_ability(self):
        import ability
        self.ability = ability.get_compactness(self)
        return self.ability

