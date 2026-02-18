import sys
import os
import re
from glob import glob
from parse import parse
from statistics import mean, stdev, median
import secrets
import json
from pathlib import Path
from itertools import zip_longest
import math
import csv

def getGraphList():
    data = []
    with open("graphlist.csv", "r") as f:
        reader = csv.reader(f, delimiter=',')
        data = list(reader)
    return data

stemParse = r"(.+)_(louvain|leiden)_Sampling_Data"

def getStats(filepath):
    with open(filepath,"r") as f:
       return json.load(f) 

def gpuBuildTable(graphs,data,outFile):
    with open(outFile,"w+") as f:
        for graph, graphSanitized in getGraphList():
            l = [graphSanitized]
            if graph in data:
                values = data[graph]
                exp = values
                #l.append("{:.0f}".format(exp["edge-cut"]["mean"]))
                l.append("{:.6f}".format(exp["modularity"]["median"]))
                l.append("{:.4f}".format(exp["total-duration-seconds"]["median"]))
                l.append("{:.4f}".format(exp["coarsen-contract-duration-seconds"]["median"]))
                l.append("{:.4f}".format(exp["leiden-refine-duration-seconds"]["median"]))
                print(" ".join(l), file=f)
            else:
                print("{} nan nan nan nan nan".format(graphSanitized), file=f)

def main():

    logDir = sys.argv[1]
    outDir = sys.argv[2]

    globMatch = "{}/*.json".format(logDir)

    data = {}
    for file in glob(globMatch):
        filepath = file
        stem = Path(filepath).stem
        stemMatch = re.match(stemParse, stem)
        if stemMatch is not None:
            graph = stemMatch.groups()[0]
            if graph not in data:
                data[graph] = {}
            data[graph] = getStats(filepath)

    graphsSorted = [key for key in data]
    graphsSorted = sorted(graphsSorted, key = str.casefold)
    gpuBuildTable(graphsSorted, data, "{}/results.txt".format(outDir))

if __name__ == "__main__":
    main()
