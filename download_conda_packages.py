#!/usr/bin/env python
# coding:utf-8

import urllib
import os
import sys
import re
import json

URLs = ["https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/",
        "https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/",
        ]


def getMainRepos(url):
    html = urllib.urlopen(url)
    repos = re.findall('title="(.+?)"', html.read())
    return repos


def getReposPkgs(url, repo):
    d = {}
    html = urllib.urlopen(os.path.join(url, repo, ""))
    plt = re.findall('title="(.+?)"', html.read())
    for p in plt:
        print("search %s platform" % p)
        u = os.path.join(url, repo, p, "")
        h = urllib.urlopen(u)
        pkgs = []
        for line in h.readlines():
            a = re.findall('title="(.+?)"', line)
            if len(a):
                pkgs.extend(a)
        pu = [os.path.join(u, i) for i in pkgs]
        d[p] = pu
    return d


def main():
    condajson = {}
    for url in URLs:
        repos = getMainRepos(url)
        reposjson = {}
        for rep in repos:
            print("search url: %s, %s repo" % (url, rep))
            repinfo = getReposPkgs(url, rep)
            reposjson[rep] = repinfo
        condajson[url] = reposjson
    with open(sys.argv[1], "w") as fi:
        json.dump(condajson, fi, indent=2)


if __name__ == "__main__":
    main()
