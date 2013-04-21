#!/usr/bin/python

import postgresql
import random
import sys
import getopt
import math
from PIL  import Image

# db informations
db_name = "madlib"
db_user = "viod"
db_server = "localhost"
db_port = 5432
db_table_name = "k_means_test"
db_field_name = "coord"

# dataset informations
ds_max_groups = 10
ds_max_x = 300
ds_max_y = 300
group_max_elts = 1000
group_max_width = 100
group_max_height = 100

default_output_file = "clustered_data.png"
db = postgresql.open("pq://" + db_user + "@" + db_server + ":" + str(db_port) + "/" + db_name)

colors = [
    (255, 0, 0), # red
    (0, 255, 0), # green
    (0, 0, 255), # blue
    (255, 255, 0), # yellow
    (0, 255, 255), # cyan
    (255, 0, 255), # pink
    (96, 0, 0), # dark_red
    (0, 96, 0), # dark_green
    (0, 0, 96), # dark_blue
    (96, 96, 96), # grey
    (0, 0, 0) # black
    ]

def create_test_table():
    """
    Create or replace the data table
    """
    try:
        db.execute("DROP TABLE IF EXISTS " + db_table_name + " CASCADE;")
    except UndefinedTableError:
        pass
    db.execute("CREATE TABLE " + db_table_name + " (" +
               "id SERIAL PRIMARY KEY, " + 
               db_field_name + " int[]" +
               ");")

def gaussian_random(lower_bound, upper_bound):
    """ 
    Generate a random number between lower_bound and upper_bound, assuming a gaussian repartition
    """
    mean = (upper_bound + lower_bound) / 2
    variance = (upper_bound - lower_bound) / 4
    x = random.gauss(mean, variance)
    while(x < lower_bound or x > upper_bound):
        x = random.gauss(mean, variance)
    return int(x)

def insert_random_data(nb_groups):
    """
    Populate the table with groups of points chosen randomly
    """
    clusters = []

    # for each group
    for i in range(nb_groups):
        width = random.randint(1, group_max_width)
        height = random.randint(1, group_max_height)
        nb_elts = random.randint(1, group_max_elts)
        min_x = random.randint(1, ds_max_x - width)
        min_y = random.randint(1, ds_max_y - height)
        clusters.append( ((min_x + width/2, min_y + height/2), []) )

        # points generation
        for j in range(nb_elts):
            x = gaussian_random(min_x, min_x + width)
            y = gaussian_random(min_y, min_y + height)
            clusters[i][1].append((x,y))
            db.execute("INSERT INTO " + db_table_name + " (" + db_field_name + ") VALUES (" +
                       "'{" + str(x) + "," + str(y) + "}');")
    return clusters

def get_points():
    """
    Get back the points previously generated
    """
    c = db.prepare("SELECT " + db_field_name + " FROM " + db_table_name + ";").declare()
    points = []
    for p in c:
        points.append(list(p[0]))
    return points

def apply_clustering_kmeans(nb_groups): 
    """
    Call to MADlib's k-means clustering function
    """
    c = db.prepare("SELECT * FROM madlib.kmeans_random('" + db_table_name + "', '" + 
                    db_field_name + "', " + str(nb_groups) + ");").declare()
    result = c.read()[0]
    centroids = result[0]
    #objective_fn = result[1]
    #frac_reassigned = result[2]
    #num_iterations = result[3]

    # init clusters
    clusters = []
    for c in centroids:
        clusters.append((c, []))

    # assign each point to its cluster
    points = get_points()
    for p in points:
        # compute distances
        distances = []
        for c in centroids:
            distances.append(math.pow(c[0] - p[0], 2) + math.pow(c[1] - p[1], 2))
        # get the indice of the nearest centroid
        nearest = 0
        for i in range(1, len(distances)):
            if(distances[i] < distances[nearest]):
                nearest = i
        clusters[nearest][1].append(p)

    return clusters

def apply_clustering_kmeanspp(nb_groups): 
    """
    Call to MADlib's k-means clustering function
    """
    c = db.prepare("SELECT * FROM madlib.kmeanspp('" + db_table_name + "', '" + 
                    db_field_name + "', " + str(nb_groups) + ");").declare()
    result = c.read()[0]
    centroids = result[0]
    #objective_fn = result[1]
    #frac_reassigned = result[2]
    #num_iterations = result[3]

    # init clusters
    clusters = []
    for c in centroids:
        clusters.append((c, []))

    # assign each point to its cluster
    points = get_points()
    for p in points:
        # compute distances
        distances = []
        for c in centroids:
            distances.append(math.pow(c[0] - p[0], 2) + math.pow(c[1] - p[1], 2))
        # get the indice of the nearest centroid
        nearest = 0
        for i in range(1, len(distances)):
            if(distances[i] < distances[nearest]):
                nearest = i
        clusters[nearest][1].append(p)

    return clusters

def export_to_png(clusters):
    """
    Visualize the result in a PNG file
    """
    def display_centroid(bitmap, x, y, color):
        """ 
        Display a big colored square to represent a centroid
        """
        # Draw a black square

        # vertical lines
        for i in max(0, int(x)-3), min(ds_max_x, int(x)+3):
            for j in range(max(0,int(y)-3),min(ds_max_y,int(y)+4)):
                bitmap[j * ds_max_x + i] = colors[10] # black
        # horizontal lines
        for i in range(max(0,int(x)-3), min(ds_max_x,int(x)+4)):
            for j in max(0,int(y)-3), min(ds_max_y, int(y)+3):
                bitmap[j * ds_max_x + i] = colors[10] # black

        # Fill this square with the color
        for i in range(max(0, int(y)-2), min(ds_max_y, int(y)+3)):
            for j in range(max(0, int(x)-2), min(ds_max_x, int(x)+3)):
                bitmap[i * ds_max_x + j] = color

    bitmap = [(255,255,255)] * ds_max_x * ds_max_y

    i = 0
    for centroid, points in clusters:
        # display points
        for p in points:
            bitmap[p[1] * ds_max_x + p[0]] = colors[i]
        # display centroid
        display_centroid(bitmap, centroid[0], centroid[1], colors[i])
        i += 1

    img = Image.new("RGB", (ds_max_x, ds_max_y))
    img.putdata(bitmap)
    return img

def parse_args(argv):
    """
    Interpret the command line
    """
    try:
        opts, args = getopt.getopt(argv, "ho:rn:", 
                               ["regen", "help", "output-file=", "nb-groups="])
    except getopt.GetOptError:
        usage()
        sys.exit(2)

    regen = False
    nb_groups = 0
    output_file = default_output_file
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(0)
        elif opt in ("-o", "--output-file"):
            output_file = arg
        elif opt in ("-r", "--regen"):
            regen = True
        elif opt in ("-n", "--nb-groups"):
            nb_groups = arg

    if(nb_groups == 0 and not regen):
        raise Exception("Please specify the number of clusters.")
    return regen, nb_groups, output_file

def generate_output(output_file, clusters_set):
    """
    Display all the clustering results on a single image
    """
    result_img = Image.new("RGB", (ds_max_x * len(clusters_set), ds_max_y))

    i = 0
    for clusters, description in clusters_set:
        tmp_img = export_to_png(clusters)
        result_img.paste(tmp_img, (i * (ds_max_x + 1), 0))
        i += 1
    result_img.save(output_file)

def usage():
    print("""
Usage:
    ./k-means_test.py -o output_file.png -n 4 -r

Options:
    -o, --output-file output_file.png:
        The resulting PNG image.
    -r, --regen:
        Generate new points. You should use it at your first run.
    -n, --nb-groups n:
        Generate n groups of points. If not generating points, classify in n 
        clusters. This argument is mandatory if you don't generate new points.
    -h, --help:
        Display this help message.
""")
          
def main(args):
    regen, nb_groups, output_file = parse_args(args)

    if(regen):
        nb_groups = random.randint(2, ds_max_groups)
        print("Creating test table...")
        create_test_table()
        print("Generating random data...")
        original_clusters = (insert_random_data(nb_groups), "Original clustering")
    else:
        pass
        
    print("Clustering data using k-means algorithm...")
    kmeans_clusters = (apply_clustering_kmeans(nb_groups), "K-means clustering")
    print("Clustering data using k-means++ algorithm...")
    kmeanspp_clusters = (apply_clustering_kmeanspp(nb_groups), "K-means++ clustering")

    print("Exporting to " + output_file + "...")
    generate_output(output_file, [ original_clusters, kmeans_clusters, kmeanspp_clusters])

    print("Done.")

if(__name__ == "__main__"):
    main(sys.argv[1:])
