
# TODO: test:       move to Jupyter Notebook
# TODO: test:       add many diagrams

import time
start_time = time.time()

import sys
sys.path.insert(0, r'd:\_NUU\2018\machine\skulls')

import data_dictionary
import numpy as np
import pandas as pd

print(f'TIME:: import libs: {time.time() - start_time:3.2f}')

data = data_dictionary.DataDictionary()
data.load_data(
    # dataset_path=r"d:\_NUU\2018\machine\skulls\init_data\test1",
    # dataset_path=r"d:\_NUU\2018\machine\skulls\init_data\skull",
    dataset_path=r"d:\_NUU\2018\machine\skulls\init_data\ionosphere",
    # dataset_path=r"d:\_NUU\2018\machine\skulls\init_data\giper",
    # dataset_path=r"d:\_NUU\2018\machine\skulls\init_data\spambase",
    # dataset_path=r"d:\_NUU\2018\machine\skulls\init_data\iris",
    # dataset_path=r"d:\_NUU\2018\machine\skulls\init_data\australian",
    metric=1,
    normalize=1,
    # delimiter=','
)

print(f"Dataset: {data.st.path.dataset};\n "
      f"Objs: {data.df.shape[0]}, features: {data.df.shape[1]}\n"
      f"metic: {data.st.metric.metric_dict[data.st.metric.default_metric]};"
      f"\tNormalizing method: {data.st.normalize.normalize_dict[data.st.normalize.default_normalize]}")
uniq = np.unique(data.labels, return_counts=True)
for n in range(len(uniq[0])): print(f"|K[{int(uniq[0][n])}]| = {uniq[1][n]}", end='; ')

data.set_border()

print(f"\nlinks: {data.link}\n\n")

#####################################
noise = data.get_noise()
print(
    f"border: len={len(data.border)}\t\t{data.border}\n"
    f"noise:  len={len(noise)}\t\t{noise}\n"
)

print(f"delete noise obj from ids. \n"
      f"BEFORE: ids.len: {len(data.ids)}")

data.ids = data.ids - noise
data.create_rel_table()
print(f"AFTER:  ids.len: {len(data.ids)}")

print(f"\nreCALC: border set\n"
      f"BEFORE: len:{len(data.border)}\tborder: {data.border}")
data.set_border()

print(f"AFTER:  len:{len(data.border)}\tborder: {data.border}")

print(f"links: {data.link}\n\n")

data.set_shell()
shell = data.get_shell()

print(f"shell: len={len(shell)}", end='\t')
shell_by_class = {int(x): 0 for x in np.unique(data.labels)}
for idn in shell: shell_by_class[int(data.labels[idn])] += 1
for item in shell_by_class.items(): print(f"|K[{item[0]}]| = {item[1]}", end='\t')
print(f"\n{shell}")

print(f"time: {time.time() - start_time:3.2f} secs")

print('\n\n*****      GROUPS     *****')
groups = data.get_groups()
print(f"len:{len(groups)}")
for el in groups:
    print(el)


print('\n\n')
ability = data.get_ability()
for el in ability:
    print(f"For Class-{int(el[0])} \t compactness = {el[1]}")
print(f"time: {time.time() - start_time:3.2f} secs\n")
print(f"\n-----------------------------------------\n")


# region STANDARD
etalon = data.get_standard(groups)
etalon_by_class = {int(x): 0 for x in np.unique(data.labels)}
for idn in etalon: etalon_by_class[int(data.labels[idn])] += 1
print(f'ETALONS: etalon.len:{len(etalon)}; ', end='')
for item in etalon_by_class.items(): print(f'|K[{item[0]}]|={item[1]}', end='; ')
print(f"\n{etalon}")
print(f"time: {time.time() - start_time:3.2f} secs")
# endregion STANDARD

# Проверка правильности подбора эталонных объектов
# Путем оценки обошающей способности
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from numpy import genfromtxt

#####################
po_etalonu = True   #
#####################

# original data
sample = genfromtxt(data.st.path.dataset, delimiter=',')
target = genfromtxt(data.st.path.label, delimiter=',')
X_train, X_test, y_train, y_test = train_test_split(sample, target, random_state=0)

# data after prepossessing
if po_etalonu:
    etalon_list = list(etalon)
    nuu_sample = data.df[etalon_list].copy()
    nuu_target = data.labels[etalon_list].copy()
else:
    ids = list(data.ids)
    nuu_sample = data.df[ids].copy()
    nuu_target = data.labels[ids].copy()
    NX_train, NX_test, Ny_train, Ny_test = train_test_split(nuu_sample, nuu_target)

print("*"*20 + "    ТЕСТЫ    " + "*"*20)
for n_neighbors in range(1, 13, 2):
    # n_neighbors = 1
    metric = data.st.metric.metric_dict[data.st.metric.default_metric]
    nuu_knn = KNeighborsClassifier(n_neighbors=n_neighbors, metric=metric)

    if po_etalonu:
        nuu_knn.fit(nuu_sample, nuu_target)
    else:
        nuu_knn.fit(NX_train, Ny_train)

    knn = KNeighborsClassifier(n_neighbors=n_neighbors, metric=metric)
    knn.fit(X_train, y_train)

    print(f"Правильность на тестовом наборе, при n={n_neighbors}:\n"
          f"Обычный: {knn.score(X_test, y_test):.4f};\t", end=' ')
    if len(etalon) > n_neighbors:
        if po_etalonu:
            print(f"NUU'кий: {nuu_knn.score(X_test, y_test):.4f}")
        else:
            print(f"NUU'кий: {nuu_knn.score(NX_test, Ny_test):.4f}")
    else:
        print(f"NUU'кий: ?")

print(f"TIME:: total {time.time() - start_time:.5} secs\n")
print(f"\n-----------------------------------------\n")

