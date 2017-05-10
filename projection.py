import sys
import pandas as pd
from sklearn.externals import joblib
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_distances

adj = joblib.load(sys.argv[1])
df = pd.DataFrame(adj).fillna(0)

X = df
names = df.index

model = TruncatedSVD(n_components=40,
                     random_state=0)
embedding = model.fit_transform(X)

print('Transforming from {} to {}'.format(df.shape, embedding.shape))
print(model.explained_variance_ratio_.sum())

###############################################################################
# Projection

senators = ['Sanders', 'Obama', 'Graham', 'Clinton', 'Rubio',
            'Frank', 'Paul', 'Kasich', 'Carson',
            'D-114', 'R-114', 'R-105']
lookup = [names.str.contains(senator).argmax() for senator in senators]
sen2vec = dict(zip(senators, [embedding[l] for l in lookup]))

print('Rubio : Median GOP :: who? : Median Dem  (Rubio - R-114 + D-144 = ?)')


# In the famous "man is to woman as king is to queen" example, queen
# is the word w that maximizes: cos(w, king) - cos(w, man) + cos(w, woman).

# Alternate Implementation:
#
# res = []
# for i, senator in enumerate(names):
#     w = embedding[i]
#     score = cosine_distances(w, sen2vec['D-114']) - \
#             cosine_distances(w, sen2vec['Obama']) + \
#             cosine_distances(w, sen2vec['Carson'])
#     res.append(score)
#
#
# res = pd.Series(res)
# sort_res = res.argsort()
#
# for i in sort_res[:3]:
#     print('Senator {} matches with {} score'.format(names[i], res[i]))

W = embedding
A = pd.Series(sen2vec['Rubio'] * len(W))
B = pd.Series(sen2vec['R-114'] * len(W))
Y = pd.Series(sen2vec['D-114'] * len(W))

score = cosine_distances(W, A) - \
        cosine_distances(W, B) + \
        cosine_distances(W, Y)

score = score.flatten()
sorted_score = score.argsort()[::-1]

for n, s in zip(names[sorted_score][:5], score[sorted_score][:5]):
    print('Senator {} matches with {} score'.format(n, s))

