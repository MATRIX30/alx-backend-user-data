#!/usr/bin/env python3
"""
module contains obfuscation function
filter_datum
"""

from typing import List
import re


def filter_datum(fields: List[str], redaction: str, message: str,
                 seperator: str) -> str:
    """function to obfusticate data"""
    for field in fields:
        message = re.sub(rf"{field}=[^{seperator}]*",
                         f"{field}={redaction}", message)
    return message