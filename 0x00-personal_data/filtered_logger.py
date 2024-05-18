#!/usr/bin/env python3
"""
module contains obfuscation function
filter_datum
"""

from typing import List
import re
def filter_datum(fields, redaction, message, separator): return re.sub(rf'({"|".join(fields)})=[^{separator}]*', lambda m: m.group().split('=')[0] + '=' + redaction, message)