# Aplikacja webowa `news`

## 🛠️ Testowanie

### 📦 Struktura katalogu testów
```
tests/                                                     
├─ acceptance.py                                        
├─ calendar_test.py                                       
├─ conftest.py                                            
├─ crime_tests.py                                         
├─ economy_tests.py                                       
├─ graph_test.py                                          
├─ integration.py                                       
├─ main_page_test.py                                      
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

#### 🧪 Testy jednostkowe (Unit Tests)
- **Cel:** Weryfikacja poprawności działania poszczególnych funkcji i metod.
- **Zakres:** Moduły takie jak `economy`, `sport`, czy `calendar`.

#### 🔗 Testy integracyjne (Integration Tests)
- **Cel:** Sprawdzenie poprawnej współpracy między różnymi modułami aplikacji.
- **Zakres:** Testowanie przepływu danych między komponentami, np. połączeń z bazą danych i API.

#### ✅ Testy akceptacyjne (Acceptance Tests)
- **Cel:** Walidacja funkcjonalności aplikacji z perspektywy użytkownika.
- **Zakres:** 
  - Weryfikacja kluczowych funkcjonalności aplikacji, np. wyświetlania wiadomości, działania kalendarza czy interakcji na stronie głównej.
  - Testy akceptacyjne są realizowane z wykorzystaniem **Selenium WebDriver**, które pozwala na automatyzację testowania interfejsu użytkownika.

#### 🌐 Testy Selenium
- **Opis:** Narzędzie Selenium WebDriver wykorzystywane jest do automatyzacji testów akceptacyjnych.
- **Zakres:**
  - Sprawdzanie poprawności wyświetlania kluczowych komponentów.
  - Weryfikacja interakcji użytkownika (np. kliknięcia).
  - Testy obejmują takie sekcje jak `news`, `weather`, czy `calendar`.

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
Testy wykonano **16.01.2025r.** na wersji aplikacji z głównego brancha `main`.
#### 📝 Podsumowanie:
Liczba testów: 62  
Testy zaliczone: ✅ 62  
Testy niezaliczone: ❌ 0  
Czas wykonania: 🕒 65.73 s.

#### 🖼️ Zrzuty ekranu:
![Zrzut ekranu](https://github.com/TobiaszAGH/news/blob/main/docs/images/testing/report_1.png)
![Zrzut ekranu](https://github.com/TobiaszAGH/news/blob/main/docs/images/testing/report_2.png)




