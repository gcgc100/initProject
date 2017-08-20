#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import shutil
import json
from sys import platform

from gClifford.mylogging import logger
from gClifford.osAddon import remember_cwd


class Project(object):

    """Project base class"""

    _allConfigs = os.path.join(os.path.dirname(__file__), "projectConfig")
    _allConfigs = os.path.abspath(_allConfigs)
    _globalConf = os.path.join(_allConfigs, "global")
    _gitignore = os.path.join(_allConfigs, "gitignore")

    def __init__(self, path, type, projectConfig=None, sub=False):
        """Init base project

        :path: project root path

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
        self._files = os.path.join(self.projectConfig, "files")

    def initProject(self):
        self.createDirs()
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
    def globalConf(self):
        return Project._globalConf

    @property
    def gitignore(self):
        return Project._gitignore

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

    @classmethod
    def listGitignores(cls):
        """ return all available gitignore files"""
        gitignoreList = os.listdir(cls._gitignore) + \
            os.listdir(os.path.join(cls._gitignore, "Global"))
        gitignoreList = set(gitignoreList) - \
            set([".git", ".github", "LICENSE",
                 "README.md", "Global", "CONTRIBUTING.md"])
        return list(gitignoreList)

    @classmethod
    def gitignorePath(cls, name):
        """Return filepath for a gitignore file """
        if name in os.listdir(cls._gitignore):
            return os.path.join(cls._gitignore, name)
        base = os.path.join(cls._gitignore, "Global")
        if name in os.listdir(base):
            return os.path.join(base, name)
        return None

    def initSubProject(self, projectName, path):
        """
        Scan the projectConfig folder,
        create subModule based on child folder
        """
        os.makedirs(os.path.join(self._path, projectName))
        Project(os.path.join(self._path, projectName), "python",
                projectConfig=path, sub=True).initProject()

    def createDirs(self):
        """Create dirs in the project """
        subconfig = self.strucs.get("sub", None)
        if subconfig is None:
            return
        projectName = subconfig[
            "projectName"].format(**self.vars)
        logger.debug("Init sub project:{0}".format(projectName))
        self.initSubProject(
            projectName, os.path.join(
                self.projectConfig, subconfig["config"]))

    def addFiles(self):
        """Add files to project
        """
        globalConf = self.globalConf
        for f in os.listdir(globalConf):
            if not self._sub:
                fullpath = os.path.join(globalConf, f)
                if os.path.isdir(fullpath):
                    shutil.copytree(fullpath,
                                    os.path.join(self._path, f))
                else:
                    shutil.copy(fullpath, self._path)
                self.addGitIgnore()

        for f in os.listdir(self._files):
            fullpath = os.path.join(self._files, f)
            if os.path.isdir(fullpath):
                shutil.copytree(fullpath,
                                os.path.join(self._path, f))
            else:
                shutil.copy(fullpath, self._path)

    def addGitIgnore(self):
        """Add .gitignore based on project type and os """
        with open(os.path.join(self._path, ".gitignore"), 'a') as gitignore:
            type = self.strucs.get("gitignore", [])
            if len(type) > 1:
                type = type[1]
            else:
                type = self._type
            typeIgnoreFile = os.path.join(
                self.gitignore,
                "{0}.gitignore".format(type))
            if os.path.isfile(typeIgnoreFile):
                with open(typeIgnoreFile, 'r') as f:
                    typeIgnore = f.read()
            else:
                typeIgnore = ""
            gitignore.write(typeIgnore)
            typeIgnoreFile = os.path.join(
                self.projectConfig,
                "{0}.gitignore".format(type))
            if os.path.isfile(typeIgnoreFile):
                with open(typeIgnoreFile, 'r') as f:
                    typeIgnore = f.read()
            else:
                typeIgnore = ""
            gitignore.write(typeIgnore)

            osMap = {"linux": "Linux",
                     "linux2": "Linux",
                     "darwin": "macOS",
                     "win32": "Windows"}
            osType = osMap.get(platform, None)
            if osType is None:
                return
            with open(os.path.join(self.gitignore,
                                   "Global/{0}.gitignore".format(osType)),
                      'r') as f:
                osIgnore = f.read()
                gitignore.write(osIgnore)

            with open(os.path.join(self.gitignore,
                                   "Global/Vim.gitignore"),
                      'r') as f:
                gitignore.write(f.read())

    def runShellCmd(self):
        """Run shell cmd in project root dir """
        with remember_cwd():
            os.chdir(self._path)
            with open(os.path.join(self.projectConfig,
                                   "shells.txt"), "r") as shells:
                for cmd in shells:
                    subprocess.call(cmd, shell=True)
