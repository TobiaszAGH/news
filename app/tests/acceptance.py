import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from .selenium_test_calendar import *
from .selenium_test_news import *
from .selenium_test_graph import *
from .selenium_weather_test import *
from .selenium_main_tests import *
