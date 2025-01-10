# Testowanie

## Fixtures

### Fixtures mockujące
- `mocked_responses` - Dostarcza mocki dla zewnętrznych zapytań HTTP

### Fixtures bazodanowe
- `crime_app` - Tworzy testową instancję aplikacji Flask
- `test_db` - Przygotowuje testową bazę danych SQLite w pamięci
- `crime_client` - Dostarcza klienta testowego
- `sample_news` - Dodaje przykładowe wiadomości do bazy
- `sample_images` - Dodaje przykładowe obrazy do bazy
- `sample_data` - Przygotowuje kompletny zestaw danych testowych

## Testy jednostkowe (Unit Tests)

### Testy modeli i bazy danych
- `test_database_connection` - Sprawdza poprawność połączenia z bazą danych
- `test_sample_news` - Weryfikuje poprawność dodawania przykładowych wiadomości
- `test_sample_images` - Weryfikuje poprawność dodawania przykładowych obrazów
- `test_sample_data` - Sprawdza poprawność zapisanych danych testowych

### Testy scrapera
- `test_fetch_article` - Testuje pobieranie artykułów
- `test_fetch_article_description` - Testuje pobieranie opisów artykułów

## Testy integracyjne (Integration Tests)

### Testy endpointów
- `test_news_home` - Sprawdza endpoint głównej strony wiadomości (/news/)
- `test_news_article` - Weryfikuje wyświetlanie pojedynczego artykułu (/news/<id>)
- `test_news_preview` - Testuje widget podglądu wiadomości (/news/news_preview)
- `test_article_not_found` - Sprawdza obsługę nieistniejących artykułów

### Testy operacji na bazie danych
- `test_save_article` - Testuje zapisywanie artykułów do bazy
- `test_save_images` - Weryfikuje zapisywanie obrazów do bazy

## Testy akceptacyjne (Acceptance Tests)

### Testy Selenium
- Testowanie interfejsu użytkownika z wykorzystaniem Selenium WebDriver
- Sprawdzanie poprawności wyświetlania komponentów
- Weryfikacja interakcji użytkownika

## Uruchamianie testów

### Testy jednostkowe
```bash
pytest app/tests/unit.py
```

### Testy integracyjne
```bash
pytest app/tests/integration.py
```

### Testy akcpetacyjne
```bash
pytest app/tests/acceptance.py
```

