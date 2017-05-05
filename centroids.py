"""
import numpy as np
from itertools import groupby

groups = groupby(adj.keys(), lambda x: x.split('-')[0])
for key, bills in groups:
    print("Averaging {}th Session".format(key))

    rep = []
    dem = []
    for bill in bills:
        voters = adj[bill].keys()
        votes = adj[bill].values()
        if "(R-" in voters:
            rep.append(adj[bill][p])
        else:
            dem.append(adj[bill][p])
    rep = np.array(rep)
    dem = np.array(dem)
"""

import numpy as np
import pandas as pd
from sklearn.externals import joblib


def compute_averages(rep, party='R'):
    # avg_rep = rep.mean()
    avg_rep = rep.median()
    grp = avg_rep.groupby(np.array(avg_rep.index.str.split('-').tolist()).T[0])

    keys = []
    averages = []

    # res = pd.DataFrame(index=avg_rep.index)

    for congress_session, average_person in grp:
        keys.append(congress_session)
        averages.append(average_person)

        # df = pd.DataFrame(average_person, index=avg_rep.index,
        #                   columns=['R-{}'.format(congress_session)])
        # print(df)
        # res = pd.concat([res, df])

    return pd.DataFrame(averages, columns=avg_rep.index,
                        index=map(lambda x: '{}-{}'.format(party, x), keys)).T
    # return pd.DataFrame(averages, index=avg_rep.index,
    #                     columns=map(lambda x: 'R-{}'.format(x), keys))


adj = joblib.load("s-voting-matrix.npy")  # h-voting-matrix
df = pd.DataFrame(adj)

mask = df.index.str.contains("\(R-")

rep = df[mask]
rep_avgs = compute_averages(rep, 'R')

dem = df[~mask]
dem_avgs = compute_averages(dem, 'D')

# print('Average Rep')
# print(rep_avgs)
#
# print('Average Dem')
# print(dem_avgs)


df = pd.concat([df.T, rep_avgs, dem_avgs], axis=1).T
# df = df.fillna(0)

print(df)

joblib.dump(df, '{}-averaged.npy'.format('s'))