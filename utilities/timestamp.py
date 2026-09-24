"""
{{PROJECT_NAME}} - Timestamp generator for output file naming.
Version: 1.0.0
Component: utilities

Exposes:
    now_stamp() -> str   -- timestamp in ddmmyy_HHMM format

External dependencies: none
"""

from datetime import datetime


def now_stamp() -> str:
    """Return current timestamp in ddmmyy_HHMM format.

    Returns:
        Timestamp string, e.g. '150126_1430'.
    """
    return datetime.now().strftime("%d%m%y_%H%M")
