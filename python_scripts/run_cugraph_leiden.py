import cugraph
import cudf
import itertools
from time import time
from statistics import median
import csv
import sys
import io
from pathlib import Path
from glob import glob
import math

def getGraphList():
    data = []
    with open("../data/graphlist.csv", "r") as f:
        reader = csv.reader(f, delimiter=',')
        data = list(reader)
    return data

def runExperiment(fname):

    with open(fname, "r") as fp:
        lines = fp.readlines()
        # pop 2 first lines because they are just metadata
        lines = lines[2:]

    lines = "\n".join(lines)
    csvf = io.StringIO(lines)
    gdf  = cudf.read_csv(csvf, delimiter=' ', names=['src', 'dst'], dtype=['int32', 'int32'])
    lines = ""

    print("finished reading {}".format(fname))

    start_g = time()

    gdf = cugraph.symmetrize_df(gdf, 'src', 'dst')
    G = cugraph.from_edgelist(gdf, source='src', destination='dst', renumber=True)
    # G = cugraph.Graph()
    # G.from_cudf_edgelist(gdf, source='src', destination='dst', renumber=True, symmetrize=True)

    n = G.number_of_vertices()
    nnz = G.number_of_edges()

    end_g = time()
    print("finished creating graph in {} seconds".format(end_g - start_g))

    times = []
    mods = []
    for i in range(5):
        try:
            start_comm = time()
            # modularity number returned is not correct
            comms, _ = cugraph.leiden(G)
            end_comm = time()
            t_time = end_comm - start_comm
            # calculate real modularity
            # slow as f
            mod = cugraph.analyzeClustering_modularity(G, comms['partition'].nunique(), comms, cluster_col_name='partition')
            times.append(t_time)
            mods.append(mod)
        except:
            times = []
            mods = []
            break
    if len(times) > 0:
        return median(times), median(mods)
    else:
        return math.nan, math.nan

def main():

    dirpath = sys.argv[1]
    logF = sys.argv[2]
    globMatch = "{}/*.mtx".format(dirpath)

    matches = {}
    for file in glob(globMatch):
        filepath = file
        stem = Path(filepath).stem
        matches[stem] = filepath

    for stem, oname in getGraphList():
        t_time, mod = runExperiment(matches[stem])
        with open(logF, "a+") as fp:
            print("{} {:6f} {:4f}".format(oname, mod, t_time), file=fp)

if __name__ == "__main__":
    main()