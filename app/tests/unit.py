from .calendar_test import (
    test_get_nameday_successful_response,
    test_get_nameday_no_nameday,
    test_get_nameday_failed_response,
    test_get_holiday_successful_response,
    test_get_holiday_no_response,
    test_holiday_failed_response,
    test_get_proverb_successful_response,
    test_get_proverb_no_response,
    test_get_agh_news_successful_response,
    test_get_agh_news_no_response,
    test_parse_date_standard,
    test_parse_date_end_of_year
)

from .news_tests import (
    test_fetch_article,
    test_fetch_article_description
)

from .sport_tests import (
    test_sport_article_model,
    test_sport_api_fetch,
    test_sport_api_fetch_error
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