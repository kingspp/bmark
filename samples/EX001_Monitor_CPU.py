# -*- coding: utf-8 -*-
"""
| **@created on:** 1/5/19,
| **@author:** prathyushsp,
| **@version:** v0.0.1
|
| **Description:**
| 
|
| **Sphinx Documentation Status:** --
|
"""

from pmark import pmonitor
import time

# Declare function and its body
@pmonitor
def random_function():
    time.sleep(5)
    x = [i**2 for i in range(1000)]
    time.sleep(5)

# Call the function
random_function()