import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from .crime_tests import (
    test_fetch_article,
    test_fetch_article_description
)

from .economy_tests import (
    test_economy_data_load,
    test_economy_data_load_swapped_dates,
    test_economy_data_load_long_period,
    test_economy_data_default,
    test_economy_data_fetch_api,
    test_fetch_link
)

from .graph_test import *

from .weather_test import (
    test_getCurrentWeather,
    test_getForecast  
)