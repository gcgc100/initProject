#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import shutil

from .Project import Project
from .Project import DirException
from gClifford.mylogging import logger


def checkPath(path):
    """Check project root path

    :path: project root path
    :returns:

    """
    if path == "":
        path = "./"
    elif not path.endswith("/"):
        path = path + "/"
    root = path
    if not os.path.exists(root):
        os.makedirs(root)
    if len(os.listdir(root)) == 0:
        return True
    else:
        print("Warning: project directory({0}) not empty.".format(root))
        return False


def initProject(path, type):
    """Init project

    :path: project root path
    :type: project type
    :returns:

    """
    try:
        project = Project.initClass(path, type)
        project.initProject()
    except DirException as e:
        logger.error(e)
        print("Project config folder not found")
        return False
    return True


def files(type):
    """Print list files list of a type of project

    :type: project type
    """
    def printTree(tree):
        for root, dirs, files in os.walk(tree):
            for f in files:
                print("{0}/{1}".format(root, f))
    p = Project(".", type)
    printTree(p.files)
    printTree(p.globalConf)


def addFile(path):
    """Add one file to current dir

    :path: filepath
    :type: project type

    """
    # filePath = os.path.join(Project(".", type).fileRoot, path)
    filePath = path
    if filePath.endswith("\n"):
        filePath = filePath[:-1]

    if filePath.endswith("gitignore"):
        filePath = Project.gitignorePath(filePath)
        if filePath is None:
            print("Can not found gitignore file")
            return
        with open(filePath, "r") as f:
            text = f.read()
        with open(".gitignore", "a") as f:
            print("Append gitignore")
            f.write(text)
        return
    if not os.path.exists(filePath):
        raise DirException("File path not exist")
        return
    if not os.path.exists(os.path.basename(filePath)):
        shutil.copy(filePath, os.path.basename(filePath))
        print("Add file:{0}".format(filePath))
        return True
    else:
        print("error: file already exists")
        return False


def main():
    if not sys.stdin.isatty():
        sys.argv.append(sys.stdin.read())
    parser = argparse.ArgumentParser("""
                                    Init Project Automatically.
                                    Create project based on config.
                                    files.txt: file list to be copyed to project
                                    struc.txt: dir tree structure
                                    sub: {"projectName": "{projectName}",
                                        "config": "module"}
                                    "projectName" accept placeholder.
                                    Could be keys of Project.vars
                                    shells.txt: shell cmds to be run
                                     """)
    parser.add_argument(
        "-t",
        "--type",
        help="Project type: {0}".format(Project.listTypes()))
    parser.add_argument(
        "-p", "--path", default="./",
        help="Project root path. Must be empty. Default:./")
    parser.add_argument(
        "-a", "--add",
        help="Add one file to current project.")
    parser.add_argument(
        "-f", "--files",
        help="Project init files.")
    parser.add_argument("--gitignores",
                        action="store_true",
                        help="List all gitignore")
    parser.add_argument("--nogit",
                        action="store_true",
                        help="Not init as a git repository if set")

    try:
        args = parser.parse_args()
    except Exception as e:
        print(e)
        sys.exit()

    if args.add:
        addFile(args.add)

    if args.type:
        checkPath(args.path)
        initProject(args.path, "global")
        initProject(args.path, args.type)

    if not args.nogit:
        initProject(args.path, "git")

    if args.files:
        files(args.files)

    if args.gitignores:
        print(Project.listGitignores())

if __name__ == "__main__":
    main()
