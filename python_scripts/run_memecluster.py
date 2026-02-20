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

executable = "./build/app/meme"
waitLimit = 1200
formatString = "Final objective: {mod:g}"
clusterFileTemp = "clustering_data{}.txt"

def getModularity(clusterFile):
    mod = 0
    with open(clusterFile,"r") as cf:
        for line in cf:
            line = line.strip()
            result = parse(formatString, line)
            if result:
                mod = float(result["mod"])
    return mod

def processGraph(input_f, oname, out_f):
    if(not os.path.exists(executable)):
        print("Error: Could not find executable {}".format(executable))
        return
    call = [executable, input_f, "101", "60"]
    call_str = " ".join(call)
    print("running {}".format(call_str), flush=True)
    clusterFile = clusterFileTemp.format(oname)
    with open(clusterFile,"w") as cf:
        process = subprocess.Popen(call, stdout=cf, stderr=cf)
        try:
            process.wait(timeout = waitLimit)
        except subprocess.TimeoutExpired:
            process.kill()
            print("Timeout reached by {}".format(call_str), flush=True)
            return
        
    mod = getModularity(clusterFile)
    with open(out_f, "a+") as fp:
        print("{} {:6f}".format(oname, mod), file=fp)


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
        processGraph(matches[stem], oname, outf)

if __name__ == "__main__":
    main()
