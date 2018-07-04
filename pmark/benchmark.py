# -*- coding: utf-8 -*-
"""
| **@created on:** 16/12/16,
| **@author:** Prathyush SP,
| **@version:** v0.0.1
|
| **Description:**
| Benchmark Module
|
| Sphinx Documentation Status:**
|
..todo::


Benchmark Statistics:
1.	Physical Memory Consumption - RAM	List[Float]	Max Physical Memory (RAM) consumed by the run in Mb/ GB - DONE
2.	Physical Memory Consumption - GPU	List[Float]	Max Physical Memory (GPU) consumed by the run in Mb/ GB
3.	Physical Processing Power Consumption	List[Float]	 Max Physical Power (CPU) consumed by the run in % - DONE
"""

__all__ = ['BenchmarkUtil', 'monitor']

import json
from collections import OrderedDict
from multiprocessing import Process
from multiprocessing.managers import BaseManager
import time
import os
import logging
from pmark.utils import generate_timestamp
from functools import wraps
import typing
from pmark.monitors import CPUMonitor, GPUMonitor, MemoryMonitor
from functools import partial

logger = logging.getLogger(__name__)


# noinspection PyMissingOrEmptyDocstring
class BenchmarkStats(object):
    """
    | **@author:** Prathyush SP
    |
    | Benchmarking Statistics
    """

    def __init__(self, benchmark_name: str):  # pragma: no cover
        self.benchmark_name = benchmark_name
        self.function_name = None
        self.function_annotations = None
        self.total_elapsed_time = None
        self.monitor_statistics = OrderedDict()
        self.timestamp = generate_timestamp()

    def get_timestamp(self):
        return self.timestamp

    def get_benchmark_name(self):
        return self.benchmark_name

    def get_monitor_statistics(self):
        return self.monitor_statistics

    def set_monitor_statistics(self, status: OrderedDict):
        self.monitor_statistics = status

    def get_total_elapsed_time(self):
        return self.total_elapsed_time

    def set_total_elapsed_time(self, t):
        self.total_elapsed_time = t

    def get_function_name(self):
        return self.function_name

    def set_function_name(self, t):
        self.function_name = t

    def get_function_annotations(self):
        return self.function_annotations

    def set_function_annotations(self, t):
        self.function_annotations = t

    def info(self):  # pragma: no cover
        return OrderedDict([
            ('benchmark_name', self.benchmark_name),
            ('timestamp', self.timestamp),
            ('function_name', self.function_name),
            ('function_annotations', self.function_annotations),
            ('total_elapsed_time (secs)', self.total_elapsed_time),
            ('monitor_statistics', self.monitor_statistics),
        ])


class BenchmarkUtil(object):
    """
    | **@author:** Prathyush SP
    |
    | Benchmark Util - 
    | Performs Training and Inference Benchmarks
    """

    def __init__(self, name: str,
                 monitors: typing.List = None,
                 writers: typing.List = None, interval_in_secs: int = None):
        """

        :param name: Util Name
        :param stats_save_path: Stats save path
        :param monitors: List of Monitors
        :param interval_in_secs:
        """
        self.name = name
        self.deployed_monitors = monitors
        self.deployed_writers = writers
        self.monitors = None
        self.writers = None
        self.benchmark_interval = interval_in_secs
        self.pid = None

    def _attach_monitors_and_writers(self, pid: int, stats):
        """
        | **@author:** Prathyush SP
        |
        | Attach Various Monitors and waits
        :param pid: Process Id
        """

        if self.deployed_monitors:
            # Initialize Monitors
            self.monitors = [
                monitor(pid=pid, interval_in_secs=self.benchmark_interval) if isinstance(monitor, type) else monitor
                for monitor in self.deployed_monitors]

            self.writers = self.deployed_writers

            # Initialize Writers
            for writer in self.writers:
                writer.initialize_writer(pid=pid, benchmark_obj=stats)

            # Start Monitors
            for monitor in self.monitors:
                monitor.start()

            # Start Writers
            for writer in self.writers:
                writer.start()

            # Wait for Monitors
            for monitor in self.monitors:
                monitor.join()

            # # Wait for Writers
            for writer in self.writers:
                writer.join()

    def _collect_monitor_stats(self):
        """
        | **@author:** Prathyush SP
        |
        | Collect Monitor Statistics
        """
        if self.monitors:
            return OrderedDict([(monitor.monitor_type, monitor.monitor_stats()) for monitor in self.monitors])
        return None

    def _collect_latest_monitor_stats(self):
        if self.monitors:
            return OrderedDict([(monitor.monitor_type, monitor.get_latest()) for monitor in self.monitors])
        return None

    def monitor(self, f=None):
        """
        | **@author:** Prathyush SP
        |
        | Value Exception Decorator.
        :param f: Function
        :return: Function Return Parameter
        """

        if f is None:
            return partial(monitor)

        # noinspection PyUnresolvedReferences
        @wraps(f)
        def wrapped(*args, **kwargs):
            start = time.time()
            logger.info('Running Benchmark - Training . . .')
            BaseManager.register('BenchmarkStats', BenchmarkStats)
            manager = BaseManager()
            manager.start()
            b_stats = manager.BenchmarkStats(self.name)
            b_stats.set_function_name(f.__name__)
            b_stats.set_function_annotations(f.__annotations__)
            try:
                p = Process(target=f, args=())
                p.start()
                self.pid = p.pid
                self._attach_monitors_and_writers(pid=p.pid, stats=self)
                p.join()
                b_stats.set_monitor_statistics(self._collect_monitor_stats())
                b_stats.set_total_elapsed_time(time.time() - start)
                # fname = self.stats_save_path + '/benchmark_{}_{}.json'.format(
                #     b_stats.get_benchmark_name().replace(' ', '_'), b_stats.get_timestamp())
                # json.dump(b_stats.info(),
                #           open(fname, 'w'), indent=2)
                # logger.info('Benchmark Util - Training completed successfully. Results stored at: {}'.format(fname))
            except ValueError as ve:
                logger.error('Value Error - {}'.format(ve))
                raise Exception('Value Error', ve)

        return wrapped

    def clean_up(self):
        """
        | **@author:** Prathyush SP
        |
        | Cleanup operations after benchmarking
        """
        pass  # pragma: no cover

monitor = BenchmarkUtil(name='',
                        # stats_save_path='/tmp/stats/',
                        monitors=[CPUMonitor, MemoryMonitor, GPUMonitor],
                        interval_in_secs=1,
                        ).monitor
