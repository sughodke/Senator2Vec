import sys
import pandas as pd
from sklearn.externals import joblib
from sklearn.manifold import TSNE
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import LSHForest
import matplotlib.pyplot as plt

# s-voting-matrix
# "s-averaged.npy"
adj = joblib.load(sys.argv[1])
df = pd.DataFrame(adj).fillna(0)

# svd = TruncatedSVD(n_components=25, n_iter=100)
# X = svd.fit_transform(df)
X = df
names = df.index

model = TruncatedSVD(n_components=40,
                     random_state=0)
embedding = model.fit_transform(X)
print(embedding.shape)
print(model.explained_variance_ratio_.sum())


###############################################################################
# Recommender

lshf = LSHForest()
X_train = embedding
lshf.fit(X_train)

senator = 'Sanders'
# senator = ['Sanders', 'Obama', 'Boxer', 'Clinton', 'Rubio', 'Frank', 'Paul']
lookup = names.str.contains(senator)

while senator != 'q':
    X_test = embedding[lookup]

    distances, indices = lshf.kneighbors(X_test, n_neighbors=6)
    print(names[indices])

    senator = input('Senator : ')
    lookup = names.str.contains(senator)

###############################################################################
# Visualization

# tsne = TSNE(n_components=2, random_state=0)
tsne = TruncatedSVD(n_components=2, random_state=0)
embedding = tsne.fit_transform(embedding)

plt.figure(1, facecolor='w', figsize=(10, 8))
# plt.clf()
# ax = plt.axes([0., 0., 1., 1.])
plt.axis('off')

# Plot the nodes using the coordinates of our embedding
for point, word in zip(embedding, names):
    plt.annotate(
        word,
        xy=(point[0], point[1]),
        ha='center',
    )
    if 'R-1' in word or 'D-1' in word:
        plt.scatter(point[0], point[1], marker='x')
    else:
        plt.scatter(point[0], point[1])

plt.show()

