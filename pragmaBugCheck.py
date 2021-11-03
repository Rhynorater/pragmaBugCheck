#!/usr/bin/env python3
import os
import sys
import glob
import re
import requests
import math

comment = """/*
-----------Compiler Bug Summary performed by pragmaBugCheck (Written by @Rhynorater)-----------
Current File Name: {}
Detected Semantic Version: {}
Detected Possible Compiler Bugs:
* {}

-----------Thanks for using pragmaBugCheck!-----------
*/"""


def roundup(x):
    return int(math.ceil(x / 100.0)) * 100

def caret(version):
    s = int("".join(version))
    bugs = []
    for sv in bugsByVersion:
        svn = int(sv.replace(".", ""))
        if (svn >= s and svn < roundup(s)):
            bugs+= bugsByVersion[sv]['bugs']
    return list(set(bugs))

def versionOnly(version):
    return bugsByVersion[".".join(version)]['bugs']

def geq(version):
    s = int("".join(version))
    bugs = []
    for sv in bugsByVersion:
        svn = int(sv.replace(".", ""))
        if (svn >= s):
            bugs+= bugsByVersion[sv]['bugs']
    return list(set(bugs))


bugsByVersion = requests.get("https://raw.githubusercontent.com/ethereum/solidity/develop/docs/bugs_by_version.json").json()

multipleRegex = "(\d+)\.(\d+)\.(\d+)"
parser = {"^\^(\d+)\.(\d+)\.(\d+)$":caret, "^=(\d+)\.(\d+)\.(\d+)$": versionOnly, "^(\d+)\.(\d+)\.(\d+)$": versionOnly, "^>=(\d+)\.(\d+)\.(\d+)$": geq}


def findFiles(directory):
    retList = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".sol"):
                retList.append(os.path.join(root, file))
    return retList

def extractPragma(files):
    retList = []
    for f in files:
        rf = open(f)
        semver = re.search("pragma solidity .+|$", rf.read()).group().lstrip("pragma solidity").rstrip(";")
        if semver:
            retList.append((f, semver))
        else:
            retList.append((f, None))
            print("Unable to find version for: "+f)
    return retList

def getBugs(pairs):
    retList = []
    for f, semver in pairs:
        if semver == None or len(re.findall(multipleRegex, semver)) > 1:
            retList.append((f, semver, "Unable to Find Version"))
            continue
        found = False
        semver = semver.replace(" ", "")
        for regex in parser:
            r = re.findall(regex, semver)
            if r:
                retList.append((f,semver, parser[regex](r[0])))
                found = True
                break
        if not found:
            retList.append((f, semver, "Unable to Parse SemVersion"))
    return retList

def writeComments(bugData):
    for fn, semversion, bugList in bugData:
        with open(fn, "r+") as f:
            content = f.read()
            f.seek(0,0)
            f.write(comment.format(fn, semversion,  "\n* ".join(bugList)) + "\n" + content)

if "--help" in sys.argv or "-h"  in sys.argv:
    print("Simply run this python script from the root directory of the project you are auditing.")
    print("Example: cd uniswap/v3-core; ~/tools/pragmaBugCheck.py")
    exit()

r = getBugs(extractPragma(findFiles(os.getcwd())))
print("-----------Compiler Bug Summary performed by pragmaBugCheck (Written by @Rhynorater)-----------")
for rd in r:
    print("""
Current File Name: {}
Detected Semantic Version: {}
Detected Possible Compiler Bugs:
* {}
""".format(rd[0], rd[1], "\n* ".join(rd[2])))
print("-----------Thanks for using pragmaBugCheck!-----------")
writeComments(r)
