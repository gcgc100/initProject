#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from sys import platform

from .Project import Project


class gitProject(Project):

    """git Project Class"""

    _gitignore = os.path.join(Project._allConfigs, "git", "gitignore")

    def __init__(self, path, projectConfig=None, sub=False):
        Project.__init__(self, path, "git", projectConfig, sub)

    @property
    def gitignore(self):
        return gitProject._gitignore

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

    def addFiles(self):
        """Add files for git. gitignore add
        """
        super(gitProject, self).addFiles()
        # self.addGitIgnore()
