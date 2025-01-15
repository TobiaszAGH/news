# Testowanie

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

