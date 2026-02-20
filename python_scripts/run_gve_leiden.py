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

executable = "./comp_exe/gve-leiden"
waitLimit = 1200
formatString = "{{{time}ms, {mark}ms mark, {init}ms init, {first}ms firstpass, {move}ms locmove, {refine}ms refine, {aggr}ms aggr, {aff} aff, {iters} iters, {passes} passes, {mod} modularity, {disc} disconnected}} leidenStaticOmp"

def getModularityAndTime(output):
    times = []
    mods = []
    for line in output.splitlines():
        result = parse(formatString, line)
        if result:
            times.append(float(result["time"]))
            mods.append(float(result["mod"]))
    return median(times) / 1000.0, median(mods)

def processGraph(input_f, stem, out_f):
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
    time, mod = getModularityAndTime(out)
    with open(out_f, "a+") as fp:
        print("{} {:6f} {:4f}".format(stem, mod, time), file=fp)


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
        processGraph(matches[stem], stem, outf)

if __name__ == "__main__":
    main()
