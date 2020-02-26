#! /usr/bin/env python3

import os
import re
import platform
import uuid
import psutil
import signal

functions = {}

def getFiles(path):
    return os.listdir(path[0])

def getSystemInfo(ignored):
    try:
        info={}
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor']=platform.processor()
        info['ram']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        return info
    except:
        return {"error": "error"}

def killProcess(args):
    os.kill(args["pid"], signal.SIGTERM)
    return {"done": "done"}

functions["files"] = getFiles
functions["sysinfo"] = getSystemInfo
functions["kill"] = killProcess

