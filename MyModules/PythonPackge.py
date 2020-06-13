# This module contains python package class definition

class PyPackage:
    def __init__(self, name, version=None):
        self.name = name
        self.version = version
        self.exported = False
        self.imported = False
