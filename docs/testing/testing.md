# Aplikacja webowa `news`

## 🛠️ Testowanie

### 📦 Struktura katalogu testów

```
tests/                                               
├─ acceptance.py                                  
├─ calendar_test.py                                 
├─ conftest.py                                                                        
├─ economy_tests.py                                 
├─ graph_test.py                                    
├─ integration.py                                 
├─ main_page_test.py
├─ news_tests.py                                 
├─ pytests.py                                       
├─ selenium_main_tests.py                           
├─ selenium_test_calendar.py                        
├─ selenium_test_graph.py                           
├─ selenium_test_news.py                            
├─ selenium_test_sport.py                           
├─ selenium_weather_test.py                         
├─ sport_tests.py                                   
├─ unit.py                                         
├─ weather_test.py                                  
└─ __init__.py
```

---

### 🎯 Strategia testowania

Każdy moduł aplikacji (np. economy, weather, news, calendar) ma swoje indywidualne testy, które weryfikują funkcje, metody. Testy te w większości stworzone zostały przy użyciu biblioteki **pytest**.

#### ⚙️ Plik 'conftest.py'

Plik `conftest.py` jest plikiem konfiguracyjnym, który zawiera ustawienia, fixtures, które są wspólne dla testów w projekcie.

Przykłady fixtures:

- **db_app** — tworzenie aplikacji testowej z bazą danych w pamięci, która pozwala na testowanie interakcji z bazą
- **mocked_responses** — fixtura do mockowania odpowiedzi z zewnętrznych API, co pozwala na testowanie aplikacji bez potrzeby rzeczywistego łączenia się z zewnętrznymi usługami
- **sample_news** i **sample_images** — fixtury przygotowujące dane testowe w postaci przykładowych artykułów i obrazów

#### 🗂️ Rodzaje testów

Testowanie naszej aplikacji webowej opiera się na trzech głównych typach testów, które odpowiadają różnym celom i poziomom analizy aplikacji.

##### 🧪 Testy jednostkowe (Unit Tests)

- **Cel:** Weryfikacja poprawności działania poszczególnych funkcji i metod.
- **Zakres:** Moduły takie jak `economy`, `sport`, czy `calendar`.

##### 🔗 Testy integracyjne (Integration Tests)

- **Cel:** Sprawdzenie poprawnej współpracy między różnymi modułami aplikacji.
- **Zakres:** Testowanie przepływu danych między komponentami, np. połączeń z bazą danych i API.

##### ✅ Testy akceptacyjne (Acceptance Tests)

- **Cel:** Walidacja funkcjonalności aplikacji z perspektywy użytkownika.
- **Zakres:** Weryfikacja kluczowych funkcjonalności aplikacji, np. wyświetlania wiadomości, działania kalendarza czy interakcji na stronie głównej.
- **Technologie:** Testy akceptacyjne są realizowane z wykorzystaniem **Selenium WebDriver**.

---

### ▶️ Uruchamianie testów

#### 🔄 Wszystkie testy

```bash
pytest app/tests/pytests.py -v
```

#### 🧪 Testy jednostkowe

```bash
pytest app/tests/unit.py -v
```

#### 🔗 Testy integracyjne

```bash
pytest app/tests/integration.py -v
```

#### ✅ Testy akcpetacyjne

```bash
pytest app/tests/acceptance.py -v
```

### 📊 Raport z testów

Testy wykonano **19.01.2025r.** na wersji aplikacji z głównego brancha `main`.

#### 📝 Podsumowanie:

Liczba testów: 71  
Testy zaliczone: ✅ 71  
Testy niezaliczone: ❌ 0  
Czas wykonania: 🕒 40 s.  


>📑 **Pełny raport** dostępny w pliku HTML:
> [tests_raport.html](https://github.com/TobiaszAGH/news/blob/main/docs/testing/tests_report.html)

#### 🖼️ Zrzuty ekranu:

![Zrzut ekranu](https://github.com/TobiaszAGH/news/blob/main/docs/images/testing/report_1.png)
![Zrzut ekranu](https://github.com/TobiaszAGH/news/blob/main/docs/images/testing/report_2.png)
![Zrzut ekranu](https://github.com/TobiaszAGH/news/blob/main/docs/images/testing/report_3.png)
