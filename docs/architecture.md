# Architektura aplikacji

Aplikacja składa się z trzech głównych warstw:

## 1. Frontend:
**Opis**:  
Warstwa frontendowa odpowiada za interfejs użytkownika. Szablony HTML są renderowane przez Flask i korzystają z frameworka CSS Bootstrap. Dodatkowe style CSS znajdują się w katalogu `static/css`.

**Technologie**:  
HTML, CSS, Bootstrap, Jinja2.

**Pliki**:  
- Szablony HTML:  
  - Główne szablony w katalogu `app/templates/`, np. `base.html` i `chart_element.html`.  
  - Szablony dla modułów znajdują się w katalogach `app/blueprints/[nazwa_modułu]/templates/`, np. `calendar.html` czy `sport.html`.
- Style CSS:  
  - Znajdują się w `app/static/css/`, np. `calendar.css`, `news.css`.

**Struktura katalogów**:
```plaintext
app/
├── templates/
│   ├── base.html
│   └── chart_element.html
├── static/
    ├── css/
    │   ├── calendar.css
    │   ├── news.css
    │   └── sport.css
    └── images/
        └── favicon.ico
```

---

## 2. Backend:
**Opis**:  
Warstwa backendowa obsługuje logikę aplikacji, przetwarzanie danych oraz komunikację z bazą danych. Aplikacja wykorzystuje Flask do zarządzania trasami i obsługi HTTP. Poszczególne funkcjonalności są zorganizowane w moduły (blueprinty), co umożliwia łatwe rozszerzanie aplikacji.

**Technologie**:  
Python, Flask, Flask-APScheduler.

**Pliki**:  
- Główne pliki backendu:  
  - `app.py` – główny plik aplikacji.  
  - `run.py` – uruchamianie aplikacji.  
  - `config.py` – konfiguracja aplikacji.  
  - `data_visualization.py` – generowanie wizualizacji danych.  
- Moduły:  
  - Znajdują się w `app/blueprints/`. Każdy moduł posiada pliki, takie jak `routes.py` (obsługa tras), `functions.py` (logika), `models.py` (definicje modeli danych).

**Struktura katalogów**:
```plaintext
app/
├── app.py
├── run.py
├── config.py
├── data_visualization.py
├── blueprints/
    ├── calendar/
    │   ├── routes.py
    │   ├── functions.py
    │   └── templates/
    │       └── calendar.html
    ├── economy/
    │   ├── routes.py
    │   ├── economyData.py
    │   └── templates/
    │       └── economy.html
    └── ...
```

---

## 3. Baza Danych:
**Opis**:  
Warstwa bazy danych przechowuje dane aplikacji. SQLAlchemy jest używane jako ORM do zarządzania bazą danych.

**Technologie**:  
SQLAlchemy

**Pliki**:  
- Konfiguracja bazy danych znajduje się w `config.py`.  
- Modele danych są definiowane w plikach `models.py` w odpowiednich modułach, np. `app/blueprints/news/models.py`.

**Struktura katalogów**:
```plaintext
app/
├── config.py
├── blueprints/
    ├── news/
    │   ├── models.py
    └── sport/
        ├── models.py
```

---

## 4. Testy:
**Opis**:  
Aplikacja zawiera zestaw testów automatycznych, które znajdują się w katalogu `app/tests/`. Testy obejmują zarówno testy jednostkowe, jak i testy integracyjne (np. Selenium).

**Pliki**:  
- Testy jednostkowe: np. `calendar_test.py`, `economy_tests.py`.  
- Testy integracyjne: np. `selenium_main_tests.py`.

**Struktura katalogów**:
```plaintext
app/
├── tests/
    ├── calendar_test.py
    ├── economy_tests.py
    ├── selenium_main_tests.py
    └── ...
```

---

## 5. Dokumentacja:
**Opis**:  
Dokumentacja aplikacji znajduje się w katalogu `docs/` i zawiera pliki, takie jak `api.md` (opis API) oraz obrazy ilustrujące działanie aplikacji.

**Struktura katalogów**:
```plaintext
docs/
├── api.md
├── architecture.md
└── images/
    ├── main.png
    └── sport_football.png
