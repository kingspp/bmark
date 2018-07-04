# -*- coding: utf-8 -*-
"""
| **@created on:** 17/11/17,
| **@author:** prathyushsp,
| **@version:** v0.0.1
|
| **Description:**
| 
|
| **Sphinx Documentation Status:** Complete
|
..todo::
    --
"""

class Writers:
    class Type:
        JsonWriter = 'json_writer'
        CustomWriter = 'custom_writer'
        CsvWriter = 'csv_writer'

class Monitors:
    class Type:
        CpuMonitor = 'cpu_monitor'
        GpuMonitor = 'gpu_monitor'
        MemoryMonitor = 'memory_monitor'

    class Code:
        Running = 'running'
        Error = 'error'
        Initializing = 'initializing'
        Disabled = 'disabled'
        Completed = 'completed'
