
# Senator2Vec

Pre-trained embeddings from US Senate voting records

I am using [GovTrack](https://www.govtrack.us/data/) (Congressional web service) to bulk download all US Senate and House of Representative votes for the **past 10 sessions of Congress**. Each voting record is stored in a JSON file.

[Link for sample JSON output](https://www.govtrack.us/data/congress/112/votes/2012/s11/data.json)

Each Senator votes Nay or Yay (or Abstain), we assign values -1 and +1 (and 0) respectively — for **each** Bill or Vote *within* each Session of Congress. We collect all these values into a “Voting Matrix.”

![Printout of Voting Matrix (+1, 0, -1 represent Yay, N/A, Nay respectively)](https://cdn-images-1.medium.com/max/4004/1*Um31rM4NvHu00uK8JfEQYA.png)*Printout of Voting Matrix (+1, 0, -1 represent Yay, N/A, Nay respectively)*

![We can see the overlap across Session of Congress when plotting the Voting Matrix](https://cdn-images-1.medium.com/max/2000/1*HrlN748xK-B7yAQaJLZfYQ.png)*We can see the overlap across Session of Congress when plotting the Voting Matrix*

Now let us try to make a meaningful embedding space. First we need a covariance matrix of the voting records

    *# Assume input data matrix X of size [N x D]*
    X **-=** np**.**mean(X, axis **=** 0) *# zero-center the data (important)*
    cov **=** np**.**dot(X**.**T, X) **/** X**.**shape[0] *# get the data covariance matrix*
> The (i,j) element of the **data covariance matrix** contains the *covariance* between i-th and j-th dimension of the data. In particular, the diagonal of this matrix contains the variances. Furthermore, the covariance matrix is symmetric and [positive semi-definite](http://en.wikipedia.org/wiki/Positive-definite_matrix#Negative-definite.2C_semidefinite_and_indefinite_matrices).

Now we run SVD to get the Eigenvectors, describing the Voting Matrix

    U,S,V **=** np**.**linalg**.**svd(cov)
> where the columns of U are the eigenvectors and S is a 1-D array of the singular values. Eigenvectors are sorted by importance, in recreating the original data.

Finally project the original voting matrix into a reduced set of eigenbasis.

    Xrot_reduced **=** np**.**dot(X, U[:,:10]) *# Xrot_reduced becomes [N x 10]*

Plotting the first two components, we can already see the spectrum of Senators. Both poticial parties are shown at the extremes. Here the scatter plot is annotate with the Senator’s name.

![Projection of Senator into 2-dimentions](https://cdn-images-1.medium.com/max/2318/1*9Bvdb2xJpHU9jAiO3QHPLg.png)*Projection of Senator into 2-dimentions*

We can take it a step further, and look at how the “median” representative from each party changes between each session of Congress.

![Blue lines point to the median of each Session, Red lines point to the median counterpart](https://cdn-images-1.medium.com/max/2318/1*U85e9bzXOHLBalybKAaTjA.png)*Blue lines point to the median of each Session, Red lines point to the median counterpart*

Pre-trained vectors can be found here:
[**sughodke/Senator2Vec**
*Senator2Vec - US Senator embeddings*github.com](https://github.com/sughodke/Senator2Vec/blob/master/transform_data.py)

## Reference

### Covariance

![](https://cdn-images-1.medium.com/max/2000/1*Nf8Clr2uAIYhGTWudt2VZA.png)

### Correlation

![](https://cdn-images-1.medium.com/max/2000/1*y_vGqQp06RdCqK8CaurxLw.png)

### PCA

![](https://cdn-images-1.medium.com/max/2000/1*APjAiKLiaA8BQmqEYoGiqw.png)

### t-SNE embeddings from Senator voting records

Similar Senators

![2D projection usng t-SNE](https://cdn-images-1.medium.com/max/3360/1*LTebCWL9_Jy0iWfuB-U6Qw.png)*2D projection usng t-SNE*

![Zoom on Senator Sanders (I-VT)](https://cdn-images-1.medium.com/max/2000/1*fqPBqIuyXwztJOZY1G3Gng.png)*Zoom on Senator Sanders (I-VT)*
