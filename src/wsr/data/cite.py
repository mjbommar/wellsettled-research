# -*- coding: utf-8 -*-
"""
The :mod:`wsr.data.cite` provides regular expressions and utilities for
identifying and parsing citations.

Author: Michael J Bommarito II <michael@bommaritollc.com>
Date: 2014-05-24
"""

# Standard imports
import re

# Basic regex
CITE_RE_NUMBER = re.compile("([0-9]+)", re.IGNORECASE | re.UNICODE)
