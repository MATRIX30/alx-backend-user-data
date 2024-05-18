#!/usr/bin/env python3
"""
module contains obfuscation function
filter_datum
"""

from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str, message: str, seperator: str) -> str:
    for field in fields:
        pattern = re.search(rf"{field}=([^{seperator}]*)", message).group(1)
        message = re.sub(pattern, redaction, message)
    return message
