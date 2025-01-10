# Aplikacja webowa `news`
Projekt na Inżynierię programowania, kierunek Nowoczene Technologie w Kryminalistyce, sem. V, grupa II, piątek 11:30.

## 📋 Opis 
`news`to  aplikacja webowa stworzow Pythone z wykorzystaiem frameworka **Flask** oraz kaskadowych arkus stylów **Bootstrap**. Projekt pokazuje, jak moża stworzyć wlomodułową aplikację webową z obsługą zewnętznego API oraz ntgracjąz bazą danych.

### Cel prjektu
Aplikacja tworzona w ramach zajęć z Inżynierii Oprogramowania za zadanie dostarczyć informacje poodowe, kyminalne i sportowe prosty i przejrzysty sposób dla użytkowników. System ma umożliwiać także wizualizację historycznych danych ogodowych i ekonomicznych. 

### Główne funkcje
- Aplikacja musi wyświetlać temerature, opady  ciśnienie dla pięciu loklizacji
- Użytkownik może przeglądać najnowsze wiadomości kryminalne dla miasta Krakowa
- Aplikacja powinna wyświetlać aktualne kursy walut
- Aplikacja umożliwia wizualizację graficzną danych historycznych o pogodzie i danych ekonomicznych
- Użytkownik może sprawdzić święta, wydarzenia na uczelni oraz imieniny

### Metodologia prowadzenia projektu
Projekt prowadzony jest w metodologi SCRUM. Szczegółowa dokumentacja prowadzenia projektu dostepna jest w [Project Plan](docs/SerwisInformacyjny-30.xlsx).

## 📐 Architektura Projektu
Aplikacja składa się z trzech głównych warstw

1. Frontend:
   **Opis**: Warstwa frontendowa odpowiada za interfejs użytkownika. Szablony HTML są renderowane przez Flask i mogą korzystać z frameworka CSS Bootstrap.
   **Technologie**: HTML, CSS, Bootstrap, Jinja2.
   **Pliki**: Znajdują się w katalogach modułów, w katalogach templates/ oraz static/.

2. Backend:
   **Opis**: Warstwa backendowa obsługuje logikę aplikacji, przetwarzanie danych oraz komunikację z bazą danych. Flask API obsługuje zapytania HTTP i zarządza trasami.
   **Technologie**: Python, Flask, Flask-APScheduler.
   **Pliki**: Znajdują się w katalogach modułów, w tym routes.py, models.py, config.py.

. Baza Danych:
   **Opis**: Warstwa bazy danych przechowuje dane aplikacji, takie jak wiadomości, dane pogodowe, kursy walut itp. SQLAlchemy jest używane jako ORM do zarządzania bazą danych.
   **Technologie**: SQLAlchemy, SQLite (lub inna baza danych).
   **Pliki**: Konfiguracja bazy danych znajduje się w config.py.

### Moduły Aplikacji
Aplikacja składa się z nastepujących modułów:
1. Moduł Główny (`main`)
- **Ścieżka** : `/`
- **Opis**: Zawiera główne trasy aplikacji, takie jak strona główna.

2. Moduł Ekonomii (`economy`)
- **Ścieżka**: `/economy`
- **Opis**: Zawiera trasy związane z ekonomią i finansami.

3. Moduł Sportu (`sport`)
- **Ścieżka**: `/sport`
- **Opis**: Zawiera trasy związane ze sportem.

4. Moduł Pogody (`weather`)
- **Ścieżka**: `/weather`
- **Opis**: Zawiera trasy związane z pogodą, w tym aktualne dane pogodowe i prognozy.

5. Moduł Wiadomości (`news`)
- **Ścieżka**: `/news`
- **Opis**: Zawiera trasy związane z wiadomościami i artykułami.

**Diagram Modułów**
```plantuml
@startuml
package "Flask Application" {
    [Flask App] --> [Bootstrap]
    [Flask App] --> [APScheduler]
    [Flask App] --> [SQLAlchemy]
    [Flask App] --> [Config]

    [Flask App] --> [Main Blueprint]
    [Flask App] --> [Economy Blueprint]
    [Flask App] --> [News Blueprint]
    [Flask App] --> [Sport Blueprint]
    [Flask App] --> [Weather Blueprint]
    [Flask App] --> [Calendar Blueprint]
}

package "Blueprints" {
    [Main Blueprint] --> [main_bp]
    [Economy Blueprint] --> [economy_bp]
    [News Blueprint] --> [news_bp]
    [Sport Blueprint] --> [sport_bp]
    [Weather Blueprint] --> [weather_bp]
    [Calendar Blueprint] --> [calendar_bp]
}

package "Config" {
    [Config] --> [db]
}

package "Scheduler" {
    [APScheduler] --> [scrape_and_save]
}
@enduml
```

### 📦 Struktura katalogów

```
├── app
│   ├── app.py
│   ├── blueprints
│   │   ├── calendar
│   │   │   ├── functions.py
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   └── templates
│   │   │       └── calendar.html
│   │   ├── economy
│   │   │   ├── economyData.py
│   │   │   ├── forms.py
│   │   │   ├── functions.py
│   │   │   ├── routes.py
│   │   │   └── templates
│   │   │       └── economy.html
│   │   ├── __init__.py
│   │   ├── main
│   │   │   ├── routes.py
│   │   │   └── templates
│   │   │       └── main.html
│   │   ├── news
│   │   │   ├── data_scraper.py
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   └── templates
│   │   │       ├── news.html
│   │   │       ├── news_preview.html
│   │   │       └── single_news.html
│   │   ├── sport
│   │   │   ├── models.py
│   │   │   ├── routes.py
│   │   │   └── templates
│   │   │       ├── articles.html
│   │   │       ├── sport.html
│   │   │       └── sport_preview.html
│   │   └── weather
│   │       ├── __init__.py
│   │       ├── routes.py
│   │       ├── templates
│   │       │   ├── weather2.html
│   │       │   ├── weather.html
│   │       │   └── weather_page.html
│   │       └── weatherService.py
│   ├── config.py
│   ├── data_visualization.py
│   ├── run.py
│   ├── static
│   │   ├── css
│   │   │   ├── calendar.css
│   │   │   ├── main.css
│   │   │   ├── news.css
│   │   │   ├── news_preview.css
│   │   │   ├── single_news.css
│   │   │   └── sport.css
│   │   └── images
│   │       └── favicon.ico
│   ├── templates
│   │   ├── base.html
│   │   └── chart_element.html
│   └── tests
│       ├── calendar_test.py
│       ├── crime_tests.py
│       ├── economy_tests.py
│       ├── graph_test.py
│       ├── __init__.py
│       ├── main_page_test.py
│       ├── pytests.py
│       ├── selenium_main_tests.py
│       ├── selenium_test_graph.py
│       └── weather_test.py
├── docs
│   ├── api.md
│   └── images
│       ├── main.png
│       └── sport_football.png
├── README.md
├── requirements.txt
```

---

### 📊 Wykorzystywane technologie

- **Flask**: Framework do budowy aplikacji webowych.
- **SQLAlchemy**: ORM do zarządzania bazą danych.
- **Jinja2**: System szablonów HTML.
- **Bootstrap**: Framework CSS do stylizacji.
- **APScheduler**: Biblioteka do zarządzania zadaniami w tle.

---

## 🚀 Instalacja i uruchomienie

### 1. Wymagania:
- **Python 3.8+**
- **Pip**
- **Virtualenv** (opcjonalnie, ale zalecane)

### 2. Instalacja:
1. Sklonuj repozytorium:
   ```bash
   git clone https://github.com/TobiaszAGH/news
   cd news
   ```

2. Utwórz i aktywuj wirtualne środowisko:
   Windows
   ```bash
   mkdir venv
   python -m venv venv
   venv\Scripts\activate
   ```
   Linux:
   ```bash
   mkdir venv
   python -m venv venv
   . ./venv/bin/activate
   ```

3. Zainstaluj wymagane zależności:
   ```bash
   pip install -r requirements.txt
   ```
### 3. Uruchomienie aplikacji:
1. Uruchom serwer:
   ```bash
   python .\app\run.py
   ```
2. Otwórz przeglądarkę i przejdź do:
   ```
   http://127..0.1:8000
   ```

---

## ⚙️ Konfiguracja

Aplikacja używa pliku `config.py` do przechowywania ustawień. Przykładowa konfiguracja:
```python
class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

Jeśli potrzebujesz niestandardowej konfiguracji, utwórz plik `.env` i zdefiniuj zmienne środowiskowe:
```env
SECRET_KEY=your_secret_key
DATABASE_URL=sqlite:///app.db
```

---

## 🛠️ Testowanie
Testy są zorganizowane w katalogu `tests/`. 
Dla Aplikacji opracowano testy jednostkowe, integracyjne i akceptacyjne.
Dla testów akceptacyjnych reazlizowanych z wykorzystaniem Selenium opracowany został plan testowania [Test Plan](docs/Acceptance_TP.xlsx).
Więcej szczegółów znajdziesz w pliku [Testing Documentation](docs/testing.md).

### Uruchomienie testów:
1. Aby uruchomić testy jednsotkowe, wykonaj:
```bash
pytest .\tests\unit
```
2. Aby uruchomić testy integracyjne, wykonaj:
```bash
pytest .\tests\integration
```

3. Aby uruchomić testy akceptacyjne, wykonaj:
```bash
pytest .\tests\acceptance
```

---

## 📖 API Dokumentacja

### API Zewnętrzne

### API Aplikacji
Szczegółowa dokumentacja API znajduje się w pliku [API Documentation](docs/api.md).

Przykładowy endpoint:

1. Endpoint: `/weather`

**GET /weather**
    - **Opis**: Pobiera aktualne dane pogodowe oraz prognozę dla domyślnego miasta (Kraków) lub miast podanych w formularzu.
    - **Metoda HTTP**: GET
    - **URL**: `/weather`
    - **Parametry**: Brak
    - **Przykład żądania**:
     ```http
    GET /weather HTTP/1.1
    Host: example.com

## 🖼️ Zrzuty ekranu

### Strona główna
![Strona główna](https://github.com/TobiaszAGH/news/blob/main/docs/images/main.png)

### Moduł sportowy
![Panel administracyjny](https://github.com/TobiaszAGH/news/blob/main/docs/images/sport_football.png)
### Moduł ekonomiczny
![Panel administracyjny](https://github.com/TobiaszAGH/news/blob/main/docs/images/economy.png)
### Moduł pogodowy
![Panel administracyjny](https://github.com/TobiaszAGH/news/blob/main/docs/images/weather.png)
---

## 👥 Autorzy

- **Tobiasz Salik** – Zwierzchnik Młyna, struktura katalogów, moduł ekonomiczny

---

## 📄 Licencja

Projekt jest udostępniony na licencji MIT. Szczegóły znajdziesz w pliku [LICENSE](LICENSE).

---

## ❓ Kontakt

Jeśli masz pytania lub problemy, napisz na:
- E-mail: m.ossysek@agh.edu.pl



projekt na inzynierie oprogramowania, grupa piatkowa 11:30
