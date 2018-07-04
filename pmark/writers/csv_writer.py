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
import time
import sys


class CsvWriter(Writer):

    def __init__(self, name: str, interval_in_secs: int, save_path='/tmp/stats', file_name: str = 'benchmark.json',
                 separator: str = ','):
        super().__init__(name=name, interval_in_secs=interval_in_secs, writer_type=constants.Writers.Type.JsonWriter)
        self.save_path = save_path

        self.file_name = file_name
        os.system('mkdir -p ' + self.save_path)
        self.fp = open(self.save_path + '/' + self.file_name, 'a')
        self.separator = separator
        self.header = None

    def write(self, stats: OrderedDict):
        if self.header is None:
            self.header = ','.join(['timestamp', *list(stats.keys()), '\n'])
            self.fp.write(self.header)
        print('Stats: ', ','.join([str(int(time.time())), *list(str(stats.values())), '\n']))
        self.fp.write(','.join([str(int(time.time())), *list([str(v) for v in stats.values()]), '\n']))
        sys.stdout.flush()

    def close(self):
        self.fp.close()
