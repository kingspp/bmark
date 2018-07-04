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
from collections import OrderedDict
import pmark.string_constants as constants
import json
from pmark.writers.writer import Writer
import os


class JSONWriter(Writer):

    def __init__(self, name:str, interval_in_secs:int, save_path = '/tmp/stats', file_name:str='benchmark.json', indent:int=2):
        super().__init__(name=name, interval_in_secs=interval_in_secs, writer_type=constants.Writers.Type.JsonWriter)
        self.save_path = save_path
        self.indent = indent
        self.file_name = file_name
        os.system('mkdir -p ' + self.save_path)
        self.fp = open(self.save_path+'/'+self.file_name, 'w')



    def write(self, stats: OrderedDict):
        json.dump(stats, self.fp, indent=self.indent)


    def close(self):
        self.fp.close()


