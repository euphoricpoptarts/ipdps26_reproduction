import sys
import os
import subprocess
from glob import glob
from pathlib import Path
from parse import parse
from statistics import median
import csv

def getGraphList():
    data = []
    with open("graphlist.csv", "r") as f:
        reader = csv.reader(f, delimiter=',')
        data = list(reader)
    return data

executable = "./comp_exe/gala"
waitLimit = 1200
modString = "final number of communities:{vtx} --> {comms} final modularity:{mod}"
timeString = "execution time without data transfer = {time}ms"
coarsenString = "Total build time = {time}ms"
clusterFileTemplate = "clustering_data_{}.txt"

def getData(fname):
    times = []
    mods = []
    builds = []
    with open(fname, "r") as f:
        for line in f:
            line = line.strip()
            result = parse(modString, line)
            if result:
                mods.append(float(result["mod"]))
            result = parse(timeString, line)
            if result:
                times.append(float(result["time"]) / 1000.0)
            result = parse(coarsenString, line)
            if result:
                builds.append(float(result["time"]) / 1000.0)

    return times, mods, builds

def processGraph(input_f, stem, oname, out_f):
    if(not os.path.exists(executable)):
        print("Error: Could not find executable {}".format(executable))
        return
    bin_f = "graphdata.bin"
    preprocess_call = ["./metis2gala", input_f, bin_f]
    print("running {}".format(" ".join(preprocess_call)), flush=True)
    subprocess.Popen(preprocess_call, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()
    call = [executable, "-f", bin_f]
    call_str = " ".join(call)
    print("running {}".format(call_str), flush=True)

    clusterFile = clusterFileTemplate.format(oname)
    with open(clusterFile,"w") as cf:
        process = subprocess.Popen(call, stdout=cf, stderr=cf)
        try:
            process.wait(timeout = waitLimit)
        except subprocess.TimeoutExpired:
            process.kill()
            print("Timeout reached by {}".format(call_str), flush=True)
            return
        
    times, mods, builds = getData(clusterFile)
    with open(out_f, "a+") as fp:
        print("{} {:6f} {:4f} {:4f}".format(oname, median(mods), median(times), median(builds)), file=fp)


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
        processGraph(matches[stem], stem, oname, outf)

if __name__ == "__main__":
    main()
