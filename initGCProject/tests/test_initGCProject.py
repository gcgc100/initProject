#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import os
import shutil
import initGCProject.initGCProject as initGCProject

from gClifford.osAddon import remember_cwd


class TestInitGCProject(unittest.TestCase):

    """Test initGCProject"""

    def setUp(self):
        self.testProject = "tests/testProject"
        os.mkdir(self.testProject)

    def tearDown(self):
        try:
            shutil.rmtree(self.testProject)
        except Exception:
            pass

    def test_checkpath(self):
        self.assertTrue(initGCProject.checkPath(self.testProject))

    def test_initPythonProject(self):
        initGCProject.initProject(self.testProject, "python")
        files = os.listdir(self.testProject)
        self.assertSetEqual(set(files),
                            set(['makefile',
                                 'tests']))

    def test_initPyModuleProject(self):
        initGCProject.initProject(self.testProject, "pymod")

    def test_initLatexProject(self):
        initGCProject.initProject(self.testProject, "latex")

    def test_initSlidesProject(self):
        initGCProject.initProject(self.testProject, "slides")

    def test_initRProject(self):
        initGCProject.initProject(self.testProject, "R")

    def test_error(self):
        ret = initGCProject.initProject("tests", "py")
        self.assertTrue(not ret)

    def test_addFile(self):
        with remember_cwd():
            os.chdir(self.testProject)
            initGCProject.addFile("../test/file")
