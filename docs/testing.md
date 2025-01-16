# Testowanie

## Struktura katalogu testów
# tests
* [.pytest_cache/](.\tests\.pytest_cache)
* [acceptance.py](.\tests\acceptance.py)
* [calendar_test.py](.\tests\calendar_test.py)
* [conftest.py](.\tests\conftest.py)
* [crime_tests.py](.\tests\crime_tests.py)
* [economy_tests.py](.\tests\economy_tests.py)
* [graph_test.py](.\tests\graph_test.py)
* [integration.py](.\tests\integration.py)
* [main_page_test.py](.\tests\main_page_test.py)
* [pytests.py](.\tests\pytests.py)
* [selenium_main_tests.py](.\tests\selenium_main_tests.py)
* [selenium_test_calendar.py](.\tests\selenium_test_calendar.py)
* [selenium_test_graph.py](.\tests\selenium_test_graph.py)
* [selenium_test_news.py](.\tests\selenium_test_news.py)
* [selenium_test_sport.py](.\tests\selenium_test_sport.py)
* [selenium_weather_test.py](.\tests\selenium_weather_test.py)
* [sport_tests.py](.\tests\sport_tests.py)
* [unit.py](.\tests\unit.py)
* [weather_test.py](.\tests\weather_test.py)
* [__init__.py](.\tests\__init__.py)


## Strategia testowania

### Testy jednostkowe (Unit Tests)

### Testy integracyjne (Integration Tests)

### Testy akceptacyjne (Acceptance Tests)

## Testy Selenium
- Testowanie interfejsu użytkownika z wykorzystaniem Selenium WebDriver
- Sprawdzanie poprawności wyświetlania komponentów
- Weryfikacja interakcji użytkownika

## Uruchamianie testów

### Wszystkie testy
```bash
pytest app/tests/pytests.py -v
```

### Testy jednostkowe
```bash
pytest app/tests/unit.py -v
```

### Testy integracyjne
```bash
pytest app/tests/integration.py -v
```

### Testy akcpetacyjne
```bash
pytest app/tests/acceptance.py -v
```

## Raport 

