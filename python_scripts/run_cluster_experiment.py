import sys
import os
import subprocess
from glob import glob
from parse import parse
from statistics import mean, stdev, median
import secrets
import json
from pathlib import Path
from itertools import zip_longest
import csv

def getGraphList():
    data = []
    with open("graphlist.csv", "r") as f:
        reader = csv.reader(f, delimiter=',')
        data = list(reader)
    return data

def printStat(fieldTitle, statList, outfile):
    min_s = min(statList)
    max_s = max(statList)
    avg = mean(statList)
    sdev = "only one data-point"
    if len(statList) > 1:
        sdev = stdev(statList)
    med = median(statList)
    print("{}: mean={}, median={}, min={}, max={}, std-dev={}".format(fieldTitle, avg, med, min_s, max_s, sdev), file=outfile)

def listToStats(statList):
    stats = {}
    stats["min"] = min(statList)
    stats["max"] = max(statList)
    stats["mean"] = mean(statList)
    stats["std-dev"] = "only one data-point"
    if len(statList) > 1:
        stats["std-dev"] = stdev(statList)
    stats["median"] = median(statList)
    return stats

def dictToStats(data):
    output = {}
    for key, value in data.items():
        if len(value) > 0 and isinstance(value[0], dict):
            d = []
            for datum in value:
                d.append(dictToStats(datum))
            output[key] = d
        elif len(value) > 0:
            output[key] = listToStats(value)
    return output


def printDict(data, outfile):
    for key, value in data.items():
        if len(value) > 0 and isinstance(value[0], dict):
            for idx, datum in enumerate(value):
                print("{} Level {}:".format(key, idx), file=outfile)
                printDict(datum, outfile)
        elif len(value) > 0:
            printStat(key, value, outfile)

def transposeListOfDicts(data):
    data = [x for x in data if x is not None]
    transposed = {}
    if len(data) == 0:
        return transposed
    #all entries should have same fields
    fields = [x for x in data[0]]
    for field in fields:
        transposed[field] = [datum[field] for datum in data]

    fieldsToTranpose = []
    for key, value in transposed.items():
        if len(value) > 0 and isinstance(value[0], list):
            fieldsToTranpose.append(key)

    for field in fieldsToTranpose:
        #value is a list of lists, transform it into list of dicts
        aligned_lists = zip_longest(*transposed[field])
        dict_list = []
        for l in aligned_lists:
            d = transposeListOfDicts(l)
            dict_list.append(d)
        transposed[field] = dict_list
    return transposed

def analyzeMetrics(metricsPath, logFile):
    with open(metricsPath, "r") as fp:
        data = json.load(fp)

    data = transposeListOfDicts(data)

    with open(logFile, "w") as output:
        printDict(data, output)

    statsDict = dictToStats(data)
    jsonFile = os.path.splitext(logFile)[0] + ".json"
    with open(jsonFile, "w") as output:
        json.dump(statsDict, output)

def runExperiment(executable, filepath, metricDir, logFile, extra_iterations):

    if(os.path.exists(logFile)):
        return

    exe_string = parse("./{}", executable)[0]
    if(not os.path.exists(exe_string)):
        print("Error: Could not find executable {}".format(exe_string))
        return
    giveup = False
    while giveup is not True:
        metricsPath = "{}/experiment_{}.txt".format(metricDir, secrets.token_urlsafe(10))
        call = [executable, "-i", filepath, "-trials", "21", "-metrics", metricsPath, "-ex_iters", extra_iterations]
        call_str = " ".join(call)
        print("running {}".format(call_str), flush=True)
        stdout_f = "/var/tmp/lp_log.txt"
        with open(stdout_f, 'w') as fp:
            process = subprocess.Popen(call, stdout=fp, stderr=subprocess.DEVNULL)
            returncode = process.wait()

        if(returncode != 0):
            if returncode != -11:
                giveup = True
            print("error code: {}".format(returncode))
            print("error produced by:")
            print(call_str, flush=True)
        else:
            analyzeMetrics(metricsPath, logFile)
            return

def processGraph(call, filepath, metricDir, logFilePrefix, extra_iterations):
    
    logFile = "{}_plouvain_Sampling_Data.txt".format(logFilePrefix)
    runExperiment(call, filepath, metricDir, logFile, extra_iterations)
    print("end {} processing".format(filepath), flush=True)

def main():

    call = sys.argv[1]
    extra_iterations = sys.argv[2]
    dirpath = sys.argv[3]
    metricDir = sys.argv[4]
    logDir = sys.argv[5]
    globMatch = "{}/*.graph".format(dirpath)

    matches = {}
    for file in glob(globMatch):
        filepath = file
        stem = Path(filepath).stem
        matches[stem] = filepath

    for stem, oname in getGraphList():
        logFile = "{}/{}".format(logDir, stem)
        processGraph(call, matches[stem], metricDir, logFile, extra_iterations)

if __name__ == "__main__":
    main()
