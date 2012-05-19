#!/usr/bin/env python
# -*- coding: utf-8 -*-

# "THE WISKEY-WARE LICENSE" (Revision 42):
# <jbc.develop@gmail.com> wrote this file. As long as you retain this notice you
# can do whatever you want with this stuff. If we meet some day, and you think
# this stuff is worth it, you can buy me a wiskey in return Juan BC

#===============================================================================
# IMPORT
#===============================================================================

import urllib2
import json
import os
import subprocess
import shlex
import shutil


#===============================================================================
# CONSTANTS
#===============================================================================

PATH = os.path.abspath(os.path.dirname(__file__))

TEMP_PATH = os.path.join(PATH, "_temp")

LIBS_PATH = os.path.join(PATH, "yatel", "libs")

MERCURIAL_REPOS = (
    {
        "name": "pilas",
        "path": "https://bitbucket.org/hugoruscitti/pilas", 
        "directory":  "pilas",
    },
)

#===============================================================================
# FUNCTIONS
#===============================================================================

def call(cmd):
    pcmd = shlex.split(cmd)
    subprocess.call(pcmd)
    

def clean():
    if os.path.exists(TEMP_PATH):
        shutil.rmtree(TEMP_PATH)


#===============================================================================
# MAIN
#===============================================================================

if __name__ == "__main__":
    clean()
    for repo in MERCURIAL_REPOS:
        
        name = repo["name"]
        path = repo["path"]
        directory = repo["directory"]
        
        print "Downloading '{}'...".format(name)
        out = os.path.join(TEMP_PATH, name)
        cmd = "hg clone {repo} {out}".format(repo=path, out=out)
        call(cmd)
        
        from_move = os.path.join(out, directory)
        to_move = os.path.join(LIBS_PATH, directory)
        
        if os.path.exists(to_move):
            shutil.rmtree(to_move)
        
        print "Intalling '{}' to libs...".format(name)
        shutil.move(from_move, to_move)
        
        cmd = "hg add {}".format(to_move)
        call(cmd)
        
    print "Cleanup".format(name)
    clean()
        
    
        
    
