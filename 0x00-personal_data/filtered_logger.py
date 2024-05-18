#!/usr/bin/env python3
"""
module contains obfuscation function
filter_datum
"""

from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str, message: str, seperator: str) -> str:
    """
    function that obfuscated log message
    Args:
                fields(List[str]) : a list of strings representing all
                                                 fields to obfuscate
                redaction(str): a string representing by what the field
                                                        will be obfuscated
                message(str): a string representing the log line
                separator: a string representing by which character is
                separating all fields in the log line (message)
    """
    for field in fields:
        pattern = rf'{field}=([^{seperator}]*)'
        pattern = re.search(pattern, message).group(1)
        message = re.sub(pattern, redaction, message)
    return message
