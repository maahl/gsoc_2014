Details about the different clustering algorithms
=================================================

This file describes the k-means algorithm, which is currently the only
clustering algorithm implemented in MADlib, and the k-medoids and
OPTICS algorithm, which I plan to implement this summer, as a GSoC
project. I'll also explain the DBSCAN algorithm, as OPTICS is only an
extension of this one.

The goal of all these algorithms is to determine clusters in a set of
points. While this problem is NP-hard, it can be solved efficiently
thanks to these algorithms, even though the result is usually not
perfect.

I've tried not to add too many details, and taken some shortcuts, so
there may be some inaccuracies. I wanted to keep this readable (not
sure that goal was achieved, though), but if anyone wants more
precisions, I'll gladly add them.

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
also pretty sensitive to outliers (points that don't obviously belong
to any cluster), and the final result depend greatly on the initial
centroids.

This algorithm doesn't work well with non-euclidean distance, in
general.

Another think to note is that k-means will result in Voronoi cell
shaped clusters, which is not always what we want.

k-medoids
---------

The k-medoids algorithm works the same way as k-means, save for a few
exceptions.

With k-medoids, the centroids are always points of the dataset (and
are then called medoids). The new medoids are the points in clusters
which minimize the sum of pairwise dissimilarities (in other terms,
the point for which the average distance to other points in the
cluster is minimal). This makes the algorithm less sensitive to
outliers than k-means.

This algorithm is computationnally more intensive than k-means, but
still fast.

As for k-means, it is possible to run the algorithm several times with
different initial centroids, and get the best result (i.e. the one
that minimizes the sum of distances from points to their centroids).

DBSCAN
-------

DBSCAN (*Density-Based Spatial Clustering of Applications with Noise*)
is a clustering algorithm based on the density of clusters.

This adresses several limitations of k-means and k-medoids: it does
not assign a cluster to outliers, and allows the detection of
weird-shaped clusters. Moreover, it doesn't need to be told the number
of clusters.

A point is called dense if enough other points are near enough from
it, where "enough other points" and "near enough" are defined by the
parameters *min_points* and *epsilon*.

*min_points* therefore represents the minimum number of points
required to make a cluster, and *epsilon* is the maximum distance a
point can be from a cluster to be considered part of this cluster.

For every unassigned point, count his *epsilon*-neighbours (not sure
this term exists, but I'll use it for convenience). If there are too
few, consider this point an outlier; else, create a new cluster and
put the current point in it, along with its neighbours, the neighbours
of its neighbours, and so on.

The main problem with DBSCAN is that it doesn't work well for clusters
with very different densities.


OPTICS
------

Bibliography
------------

http://en.wikipedia.org where clustering algorithms are well detailed

http://www.stat.cmu.edu/~ryantibs/datamining/lectures/04-clus1-marked.pdf

http://www.vitavonni.de/blog/201211/2012110201-dbscan-and-optics-clustering.html
