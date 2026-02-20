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

executable = "./comp_exe/v-louvain"
waitLimit = 1200
formatString = "{{{threads} threads}} -> {{{time}ms, {mark}ms mark, {init}ms init, {first}ms first, {move}ms move, {aggr}ms aggr, {iters} iters, {passes} passes, {mod} modularity}} louvainStaticCuda"

def getModularityAndTime(output):
    times = []
    mods = []
    coarsen = []
    for line in output.splitlines():
        if "louvainStaticCuda" in line:
            result = parse(formatString, line)
            times.append(float(result["time"]))
            mods.append(float(result["mod"]))
            coarsen.append(float(result["aggr"]))
    return median(times) / 1000.0, median(mods), median(coarsen) / 1000.0

def processGraph(input_f, oname, out_f):
    if(not os.path.exists(executable)):
        print("Error: Could not find executable {}".format(executable))
        return
    call = [executable, input_f, "1"]
    call_str = " ".join(call)
    print("running {}".format(call_str), flush=True)
    process = subprocess.Popen(call, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    try:
        process.wait(timeout = waitLimit)
    except subprocess.TimeoutExpired:
        process.kill()
        print("Timeout reached by {}".format(call_str), flush=True)
        return
    
    out, _err = process.communicate()
    out = out.decode("utf-8")
    time, mod, coarsen = getModularityAndTime(out)
    with open(out_f, "a+") as fp:
        print("{} {:6f} {:4f} {:4}".format(oname, mod, time, coarsen), file=fp)


def main():

    input_dirpath = sys.argv[1]
    outf = sys.argv[2]
    globMatch = "{}/*.mtx".format(input_dirpath)

    matches = {}
    for file in glob(globMatch):
        filepath = file
        stem = Path(filepath).stem
        matches[stem] = filepath

    for stem, oname in getGraphList():
        processGraph(matches[stem], oname, outf)

if __name__ == "__main__":
    main()
