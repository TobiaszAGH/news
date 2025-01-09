import pytest

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from .selenium_main_tests import *
from .selenium_test_graph import *