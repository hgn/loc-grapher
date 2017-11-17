#!/usr/bin/env python3

import tempfile
import shutil
import subprocess
import json
import matplotlib
import matplotlib.pyplot as plt

REPO = "https://github.com/hgn/captcp.git"


def clone(tmpdir):
    cmd = "git clone {} {}".format(REPO, tmpdir)
    w = subprocess.Popen(cmd.split())
    w.wait()

def tags(tmpdir):
    cmd = 'git -C {} tag'.format(tmpdir)
    result = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    tags = result.stdout.decode('utf-8').splitlines()
    return sorted(tags)

def checkout(tmpdir, tag):
    cmd = "git -C {} checkout {}".format(tmpdir, tag)
    w = subprocess.Popen(cmd.split())
    w.wait()

def cloc(tmpdir):
    cmd = 'cloc --json {}'.format(tmpdir)
    result = subprocess.run(cmd.split(), stdout=subprocess.PIPE)
    cloc = result.stdout.decode('utf-8')
    return json.loads(cloc)

def graph(tags, data):
    dpi = 300
    #plt.figure(figsize=(20,10))
    #plt.figure(num=None, figsize=(80, 60), dpi=200, facecolor='w', edgecolor='k')
    matplotlib.rcParams.update({'font.size': 4})
    plt.figure(figsize=(1200 / dpi, 800 / dpi), dpi=dpi, facecolor='w', edgecolor='k', frameon=False)
    x = list(); y = list(); labels = list()
    for i, tag in enumerate(tags):
        x.append(i)
        y.append(data[tag]['SUM']['code'])
        labels.append(tag)
    plt.plot(x, y)
    plt.xticks(x, labels, rotation='vertical')
    # Pad margins so that markers don't get clipped by the axes
    # Tweak spacing to prevent clipping of tick-labels
    plt.margins(.2)
    plt.subplots_adjust(bottom=0.15)
    plt.ylabel('Lines of Code')
    plt.xlabel('Release')
    plt.savefig('cloc.png', dpi=dpi)



if __name__ == "__main__":
    tmp_dir = "/tmp/foo"
    shutil.rmtree(tmp_dir, ignore_errors=True)
    #tmp_dir = tempfile.TemporaryDirectory(delete=False)
    print(tmp_dir)
    clone(tmp_dir)
    tags = tags(tmp_dir)
    data = dict()
    for tag in tags:
        print(tag)
        checkout(tmp_dir, tag)
        data[tag] = cloc(tmp_dir)
    graph(tags, data)
