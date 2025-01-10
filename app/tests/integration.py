import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from .calendar_test import (
    test_get_nameday_successful_response,
    test_get_nameday_no_nameday,
    test_get_nameday_failed_response,
    test_get_holiday_successful_response,
    test_get_holiday_no_holiday,
    test_get_holiday_failed_response,
    test_get_proverb_successful_response
)

from .crime_tests import (
    test_database_connection,
    test_sample_news,
    test_sample_images,
    test_sample_data,
    test_save_article,
    test_save_images,
    test_news_home,
    test_news_article,
    test_news_preview,
    test_article_not_found
)

from .economy_tests import (
    test_economy_endpoint,
    test_start_after_end,
    test_correct_economy,
    test_over_93_days
)

from .main_page_test import (
    test_home_page,
    test_404_page
)

from .weather_test import (
    test_hello_endpoint
)