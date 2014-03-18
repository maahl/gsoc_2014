GSoC 2014 proposal: implementing clustering algorithms in MADlib
================================================================

Synopsis
--------

This project aims to implement some clustering algorithms in MADlib,
which is a data analytics and machine learning library for PostgreSQL,
Greenplum and HAWQ.

Benefits to the PostgreSQL community
------------------------------------

Currently, only the k-means clustering algorithm is implemented in
MADlib (see `Link the doc
<http://doc.madlib.net/latest/group__grp__clustering.html>`). The
k-medoids algorithm, while being computationnally more intensive, is
much less sensitive to outliers (points that don't belong obviously to
one cluster or another). This is interesting on noisy datasets, that's
why I'm planning to implement it during the first part of the GSoC.

Still, these algorithms are based on distance computation, therefore
they can only find convex clusters. That's why I'm proposing to
implement the `Link OPTICS
<http://en.wikipedia.org/wiki/OPTICS_algorithm>` (*ordering points to
identify the clustering structure*), which addresses this
issue, as the second part of this GSoC project.

The PostgreSQL community would benefit from these features, as it
would make available clustering algorithms more powerful than simple
k-means.

Project details
---------------

k-medoids
"""""""""

The first goal of this project is to implement the k-medoids
clustering algorithm. For this, I'll first spend some time studying
the k-means algorithm, as both will probably be pretty similar. This
will also allow me to get familiar with the codebase, the conventions,
the data structures I'll need, etc.

Then I'll implement, test and debug the algorithm. If relevant, I'll
also provide a "k-medoids++" version, which, similarly to the
k-means++ function in MADlib, will chose the initial centroids
depending on the dataset, instead of chosing them randomly. This
allows to detect small clusters located far from the others (which are
usually detected as part of an other bigger cluster using the standard
algorithm).

The final step would be to refactor the code from k-means and
k-medoids to remove any code duplication introduced in this first
part.

OPTICS
""""""

The second part of this project would be to implement the
density-based clustering algorithm OPTICS, which would overcome the
main problem of both the k-means and k-medoids algorithm: non-convex
clusters. This algorithm has been preferred over `Link DBSCAN
<http://en.wikipedia.org/wiki/DBSCAN>` as it is able to detect
clusters of different densities, and, consequently, overlapping
clusters.

I'll first take some time to understand full well the algorithm, and
make a prototype in Python, to be sure I know how it works. Then I'll
actually implement it, test it, and debug it in MADlib.

If, after that, any time's left, I'll consider implementing some
of the improvements of k-means and k-medoids that we can find in the
litterature.

Deliverables
------------

* the k-medoids algorithm in MADlib;
* the OPTICS algorithm, also in MADlib;
* optionnally, some improvements on k-means and/or k-medoids.

Project Schedule
----------------

#. Implementation of the k-medoids algorithm: from 19/05 to 30/05
#. Tests, debug and doc of k-medoids: from 31/05 to
   13/06
#. Prototype of OPTICS in Python: from 14/06 to 18/06
#. Actual implementation of OPTICS in MADlib: from 19/06 to 25/06
#. Tests, debug and doc of OPTICS: from 25/06 to 11/06
