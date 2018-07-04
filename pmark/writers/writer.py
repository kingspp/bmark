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

from threading import Thread
from abc import ABCMeta, abstractmethod
from collections import OrderedDict
import time
import pmark.string_constants as constants
import psutil
import logging
import traceback

logger = logging.getLogger(__name__)


class Writer(Thread, metaclass=ABCMeta):
    """

    """

    def __init__(self, name: str, writer_type: constants.Writers.Type, interval_in_secs: int):
        super().__init__()
        self.name = name
        self.benchmark_util = None
        self.type = writer_type
        self.interval_in_secs = interval_in_secs
        self.process_status = None
        self.psutil_process = None
        self.pid = None
        self.validate()

    def _check_process_status(self):
        """
        | **@author:** Prathyush SP
        |
        | Check status of pid which is monitored
        :return: True / False based on conditions
        """
        self.process_status = self.psutil_process.status()
        return psutil.pid_exists(self.pid) and self.psutil_process.is_running() \
               and not (self.psutil_process.status() == psutil.STATUS_ZOMBIE
                        or self.psutil_process.status() == psutil.STATUS_DEAD
                        or self.psutil_process.status() == psutil.STATUS_STOPPED)

    def initialize_writer(self, pid: int, benchmark_obj):
        """

        :param pid:
        :param benchmark_obj:
        :return:
        """
        self.pid = pid
        self.benchmark_util = benchmark_obj

    @abstractmethod
    def close(self):
        pass

    @abstractmethod
    def write(self, stats: OrderedDict):
        pass

    def run(self):
        if psutil.pid_exists(self.pid):
            self.psutil_process = psutil.Process(self.pid)
            self.process_status = constants.Monitors.Code.Initializing
        else:
            logger.debug('Process does not exist')
            self.process_status = 'ERROR'

        try:
            while self._check_process_status():
                self.write(self.benchmark_util._collect_latest_monitor_stats())
                time.sleep(self.interval_in_secs)
        except psutil._exceptions.NoSuchProcess:
            self.close()
            self.process_status = constants.Monitors.Code.Completed
            logger.debug('Completed. Stopping {}'.format(self.type))
        except Exception as e:
            self.close()
            self.process_status = constants.Monitors.Code.Error
            logger.debug('Encountered {}. Stopping {}'.format(e, self.type))
            print(traceback.format_exc())
            exit()

    def validate(self):
        if self.interval_in_secs < 1:
            self.interval_in_secs = 1
            logger.debug('Minimum supported interval is 1 seconds')
