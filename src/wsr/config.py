# -*- coding: utf-8 -*-
"""
The :mod:`wsr.config` handles configuration for the Well-Settled Research
(WSR) project.

Author: Michael J Bommarito II <michael@bommaritollc.com>
Date: 2014-05-24
"""

# Standard imports
import os

# Path configuration
BASE_PATH = "/workspace/wellsettled-research/"
DATA_PATH = os.path.join(BASE_PATH, "data")
SCRATCH_PATH = os.path.join(BASE_PATH, "scratch")
RESULTS_PATH = os.path.join(BASE_PATH, "results")

# Dataset paths
SCOTUS_FILE_NAME = os.path.join(DATA_PATH,
                              "supreme_court_of_the_united_states.zip")

# QA paths
QA_PATH = os.path.join(BASE_PATH, "qa")
QA_SCOTUS_PATH = os.path.join(QA_PATH, "scotus")

try:
    from .local_config import *
except ImportError:
    pass
