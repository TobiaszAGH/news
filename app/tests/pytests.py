import pytest

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from .main_page_test import *
from .selenium_main_tests import *
from .selenium_test_graph import *
from .graph_test import *
from .weather_test import *
from .economy_tests import *
from .sport_tests import *
from .crime_tests import *
from .calendar_test import *


from app import app as original_app


@pytest.fixture
def client():
    app = original_app
    app.config['TESTING'] = True
    return app.test_client()

