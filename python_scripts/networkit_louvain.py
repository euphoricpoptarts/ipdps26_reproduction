from networkit import *
from time import time
import sys
from glob import glob
from pathlib import Path
from statistics import median
import csv

def getGraphList():
    data = []
    with open("graphlist.csv", "r") as f:
        reader = csv.reader(f, delimiter=',')
        data = list(reader)
    return data

def testGraph(graph_f):
    g = readGraph(graph_f, Format.METIS)

    times = []
    mods = []
    for i in range(21):
        comm = community.PLM(g)

        start = time()

        comm.run()

        total_time = time() - start
        times.append(total_time)

        part = comm.getPartition()

        mod = community.Modularity().getQuality(part, g)
        mods.append(mod)
    return median(times), median(mods)

def main():

    input_dirpath = sys.argv[1]
    outf = sys.argv[2]
    globMatch = "{}/*.graph".format(input_dirpath)

    matches = {}
    for file in glob(globMatch):
        filepath = file
        stem = Path(filepath).stem
        matches[stem] = filepath

    for stem, oname in getGraphList():
        print(oname)
        time, mod = testGraph(matches[stem])
        with open(outf, "a+") as fp:
            print("{} {:6f} {:4f}".format(oname, mod, time), file=fp)

if __name__ == "__main__":
    main()