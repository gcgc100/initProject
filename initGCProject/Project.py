#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import shutil
import json

from gClifford.mylogging import logger
from gClifford.osAddon import remember_cwd


class DirException(Exception):
    pass


class Project(object):

    """Project base class"""

    _allConfigs = os.path.join(os.path.dirname(__file__), "projectConfig")
    _allConfigs = os.path.abspath(_allConfigs)

    @classmethod
    def initClass(cls, path, type, projectConfig=None, sub=False):
        """Init base project

        :path: project root path
        :type: project type
        :projectConfig: project config file directory
        :sub: whether is subproject(unused)

        """
        from gitProject import gitProject
        if type == "git":
            return gitProject(path, projectConfig, sub)
        else:
            return Project(path, type, projectConfig, sub)

    def __init__(self, path, type, projectConfig=None, sub=False):
        """Init base project

        :path: project root path
        :type: project type
        :projectConfig: project config file directory
        :sub: whether is subproject(unused)

        """
        if not path.endswith("/"):
            path = path+"/"
        self._path = os.path.abspath(path) + "/"
        self._type = type
        self._sub = sub
        self._struc = None
        if projectConfig is None:
            self.projectConfig = os.path.join(Project._allConfigs, type)
        else:
            self.projectConfig = projectConfig
        if not os.path.exists(self.projectConfig):
            raise DirException("Directory not exist")
        self._files = os.path.join(self.projectConfig, "files")

    def initProject(self):
        self.addFiles()
        self.runShellCmd()

    @property
    def files(self):
        return os.path.join(self.projectConfig, "files")

    @property
    def fileRoot(self):
        return self.projectConfig

    @property
    def projectName(self):
        return os.path.basename(os.path.dirname(self._path))

    @property
    def vars(self):
        """Available vars in str
        """
        return {"projectName": self.projectName}

    @property
    def strucs(self):
        """Load strucs from struc.txt file """
        if self._struc is not None:
            return self._struc
        with remember_cwd():
            self._struc = {}
            with open(os.path.join(self.projectConfig, "struc.txt")) as f:
                for l in f:
                    if l.startswith("#"):
                        continue
                    try:
                        sepIndex = l.index(":")
                        key = l[:sepIndex].strip()
                        value = json.loads(l[sepIndex+1:])
                        self._struc[key] = value
                    except ValueError as e:
                        logger.error(e)
                        self._struc = {}
        return self._struc

    @classmethod
    def listTypes(cls):
        """ return available project type list """
        typeList = os.listdir(cls._allConfigs)
        typeList = set(typeList) - set([".ropeproject", "gitignore", "global"])
        return list(typeList)

    def addFiles(self):
        """Add files to project
        """
        for f in os.listdir(self._files):
            fullpath = os.path.join(self._files, f)
            if os.path.isdir(fullpath):
                shutil.copytree(fullpath,
                                os.path.join(self._path, f))
            else:
                shutil.copy(fullpath, self._path)

    def runShellCmd(self):
        """Run shell cmd in project root dir """
        with remember_cwd():
            os.chdir(self._path)
            with open(os.path.join(self.projectConfig,
                                   "shells.txt"), "r") as shells:
                for cmd in shells:
                    subprocess.call(cmd, shell=True)
