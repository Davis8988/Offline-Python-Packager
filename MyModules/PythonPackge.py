# This module contains python package class definition


class PyPackage:
    def __init__(self, name, version=None):
        self.name = name
        self.version = version
        self.exported = False
        self.imported = False
        self.full_name = self._get_pkg_full_name()

    def _get_pkg_full_name(self):
        return "{}=={}".format(self.name, self.version) if self.version else self.name
