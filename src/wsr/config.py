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
BASE_PATH="./"
DATA_PATH=os.path.join(BASE_PATH, "data")
SCOTUS_FILE_NAME=os.path.join(DATA_PATH,
                              "supreme_court_of_the_united_states.zip")