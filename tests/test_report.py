import pytest

from simpletimeit.datatypes import Report
from simpletimeit import report
try:
    from unittest.mock import Mock, patch
except ImportError:
    from mock import Mock, patch
