"""
checking abilities of the model
"""

import numpy as np


def get_compactness_NEEDTOREWORK(instance):
    """
    Calculates ability of the model [0..1]. 1=ideal
    :param instance: === instance of data_dict
    :return:         === tuple of l*2 size. l = classes count
    """

    # проверка КОМПАКТНОСТИ
    # mi  число obj в классе
    # mij число obj в группе
    compactness = list()

    labels, counts = np.unique(instance.labels, return_counts=True)

    for label in zip(labels, counts):
        label_name = label[0]
        mi = int(label[1])
        summa = 0.
        for g in instance.groups:
            if instance.labels[int(next(iter(g)))] == label_name:
                summa += len(g) ** 2
        Qi = summa / (mi ** 2)
        compactness.append((label_name, Qi))
        # print(f"Class:{label_name}, \tQi={Qi:1.4}")

    return compactness


def get_compactness(instance):
    """
    Calculates ability of the model [0..1]. 1=ideal
    :param instance: === instance of data_dict
    :return:         === tuple of (l+1)*2 size. l = classes count.
                     === last row for general compactness of dataset
    """

    # проверка КОМПАКТНОСТИ
    # mi  число obj в классе i
    # mij число obj в группе j класса i
    compactness = list()
    m = g_compactness = 0.

    labels = np.unique(instance.labels, return_counts=True)

    for label in labels:  # for each label
        label_name = label[0]   #
        mi = int(label[1])      # power of label

        summa = 0.
        for g in instance.groups:  # for each group of label
            if instance.labels[int(next(iter(g)))] == label_name:
                summa += len(g) ** 2
        Qi = summa / (mi ** 2)
        compactness.append((label_name, Qi))
        g_compactness += mi * Qi
        m += mi

    ##############################################################
    #  General compactness for all  ##############################
    ##############################################################
    compactness.append(('general', g_compactness / m))

    return compactness

# TODO: ability: add other abilities

