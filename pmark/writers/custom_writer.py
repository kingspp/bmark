# -*- coding: utf-8 -*-
"""
| **@created on:** 02/07/18,
| **@author:** prathyushsp,
| **@version:** v0.0.1
|
| **Description:**
| 
|
| **Sphinx Documentation Status:** --
|
..todo::
"""
from collections.__init__ import OrderedDict

from pmark.writers.writer import Writer
import pmark.string_constants as constants
import typing


class CustomWriter(Writer):
    def __init__(self, name: str, interval_in_secs: int, callable_fn: typing.Callable):
        super().__init__(name=name, writer_type=constants.Writers.Type.CustomWriter,
                         interval_in_secs=interval_in_secs)
        self.callable_fn = callable_fn

    def write(self, stats: OrderedDict):
        self.callable_fn(stats)

    def close(self):
        pass
