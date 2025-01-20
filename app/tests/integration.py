from .calendar_test import (
    test_calendar_preview
)

from .news_tests import (
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

from .sport_tests import (
    test_sport_home_with_articles,
    test_sport_home_article_no_image,
    test_sport_home_filter_discipline,
    test_sport_home_filter_no_results,
    test_sport_preview
)

from .economy_tests import (
    test_economy_endpoint,
    test_start_after_end,
    test_correct_economy,
    test_over_93_days
)

from .main_page_test import *

from .weather_test import (
    test_hello_endpoint
)