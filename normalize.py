"""
There we will use <нормировка> functions
"""

import datetime
import time
# TODO: normalize:      move normalize function to this file


def get_normalized_df(instance):
    # NEED validate method

    if instance.st.normalize.default_normalize == 0:
        return instance.df
    elif instance.st.normalize.default_normalize == 1:
        return method1(instance)
    elif instance.st.normalize.default_normalize == 4:
        return method4(instance)


def method1(instance):
    """ X[i][j] = ( X[i][j] - min(X[:,j]) ) / ( max(X[:,j]) - min(X[:, j]) )

    :param instance:    instance of DD
    :return:            df = dataframe
    """
    df = instance.df.copy()  # dataframe === m*n size array
    m, n = df.shape

    # region LOG_FILES
    log = instance.st.logging
    start_time = time.time()
    if log:
        normalize_file = open(instance.st.path.normalize_log, mode='w')
        normalize_file.write(str(datetime.datetime.now()))
        normalize_file.write(
            f"\n\nnormalizing with method "
            f"{instance.st.normalize.normalize_dict[instance.st.normalize.default_normalize]}"
            f"\n\ninitial dataframe:\n {instance.df[:]}\n")
    # endregion LOG_FILES

    errors = []
    for feature_no in range(n):
        minimum_value = min(df[:, feature_no])
        maximum_value = max(df[:, feature_no])

        if minimum_value != maximum_value:
            for idn in range(m):
                df[idn][feature_no] = (df[idn][feature_no] - minimum_value) / \
                                      (maximum_value - minimum_value)
        else:
            errors.append([feature_no, minimum_value, maximum_value])
            for idn in range(m):
                df[idn][feature_no] = (df[idn][feature_no] - minimum_value)

        if log:
            normalize_file.write(f"feature number {feature_no}, "
                                 f"max={maximum_value}, min={minimum_value}\n")

    if errors:
        if log:
            normalize_file.write(f"\n::ERROR::\n")
            for item in errors:
                normalize_file.write(f"on feature number: {item[0]}. "
                                     f"max={item[2]} = min={item[1]}\n")
    if log:
        normalize_file.write(f"\nnormalized dataframe:\n{df[:]}"
                             f"\n\nTIME:: time spend: {time.time() - start_time:.3f}"
                         )

    return df


def method4(instance):
    """ X[i][j] = X[i][j] / max(X[:,j]

    :param instance:    instance of DD
    :return:            normalized df = dataframe
    """
    start_time = time.time()
    df = instance.df.copy()  # dataframe === m*n size array
    m, n = df.shape

    # region LOG_FILES
    normalize_file = open(instance.st.path.normalize_log, mode='w')
    normalize_file.write(str(datetime.datetime.now()))
    normalize_file.write("\n\n")

    normalize_file.write(
        f"normalizing with method"
        f"{instance.st.normalize.normalize[instance.st.normalize.default_normalize]}"
        f"\n\ninitial dataframe:\n {df[:]}\n")
    # endregion LOG_FILES

    for feature_no in range(n):
        maximum_value = max(df[:, feature_no])

        for idn in range(m):
            df[idn][feature_no] = df[idn][feature_no] / maximum_value
    normalize_file.write(f"\nnormalized dataframe:\n{df[:]}"
                         f"\n\nTIME:: time spend: {time.time() - start_time:.3f}")

    return df

