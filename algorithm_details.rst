Details about the different clustering algorithms
=================================================

This file describes the k-means algorithm, which is currently the only
clustering algorithm implemented in MADlib, and the k-medoids and
OPTICS algorithm, which I plan to implement this summer, as a GSoC
project. I'll also explain the DB-SCAN algorithm, as OPTICS is only an
extension of this one.

The goal of all these algorithms is to determine clusters in a set of
points. While this problem is NP-hard, it can be solved efficiently
thanks to these algorithms, even though the result is usually not
perfect.

k-means
-------

The k-means algorithm is the one implemented in MADlib. It selects
*k* points, either randomly, among the dataset, or set by the user,
to use as initial centroids (center of clusters). *k* must be
defined by the user; the algorithm is unable to guess the number of
clusters.

All the points in the dataset are then affected to the nearest
centroid, thus making *k* clusters.

The next step is to compute the new centroids as a "mean" of all the
points in a cluster. Then reassign all the points to then new
centroids, and start all over again until there is no change in
cluster assignation.

This algorithm is usually pretty fast (even though it can be made to
take an exponential time to converge). Still, it is easy to get a
wrong result because of local convergence, e.g. having one cluster
split in two parts by the algorithm, or two clusters merged. It is
also pretty sensitive to outliers.

This algorithm doesn't work well with non-euclidean distance, also.

k-medoids
---------

DB-SCAN
-------

OPTICS
------

Bibliography
------------

http://en.wikipedia.org
http://www.stat.cmu.edu/~ryantibs/datamining/lectures/04-clus1-marked.pdf
