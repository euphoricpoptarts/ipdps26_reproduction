import sys
import subprocess
from glob import glob
from pathlib import Path
import csv

def getGraphList():
    data = []
    with open("graphlist.csv", "r") as f:
        reader = csv.reader(f, delimiter=',')
        data = list(reader)
    return data

def processGraph(input_f, output_f):
    preprocess_call = ["./metis2mtx", input_f, output_f]
    print("Running {}".format(" ".join(preprocess_call)))
    subprocess.Popen(preprocess_call, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).wait()


def main():

    input_dirpath = sys.argv[1]
    output_dirpath = sys.argv[2]
    globMatch = "{}/*.graph".format(input_dirpath)

    matches = {}
    for file in glob(globMatch):
        filepath = file
        stem = Path(filepath).stem
        matches[stem] = filepath

    for stem, oname in getGraphList():
        processGraph(matches[stem], "{}/{}.mtx".format(output_dirpath, stem))

if __name__ == "__main__":
    main()
