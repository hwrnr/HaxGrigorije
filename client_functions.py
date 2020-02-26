#! /usr/bin/env python3

import os

functions = {}

def getFiles(path):
    return os.listdir(path[0])

functions["files"] = getFiles
